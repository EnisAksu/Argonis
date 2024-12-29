import requests
from datetime import datetime
from pathlib import Path
import time
import concurrent.futures
import sys
import logging
import traceback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('threat_intel.log')
    ]
)
logger = logging.getLogger(__name__)

class ThreatIntelCollector:
    def __init__(self):
        try:
            self.data_dir = Path(".")
            if not self.data_dir.exists():
                self.data_dir.mkdir(parents=True, exist_ok=True)
                
            # Updated C2 Intel Feeds URLs - Verified Working
            self.c2_feeds = {
                "CobaltStrike-TPs": "https://threatview.io/Downloads/High-Confidence-CobaltStrike-C2%20-Feeds.txt",
                "cyber_crime_tracker": "https://cybercrime-tracker.net/all.php"
            }
            
            # Verified Working Base Feeds
            self.base_feeds = {
                "ips": [
                    "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
                    "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt",
                    "https://lists.blocklist.de/lists/all.txt",
                    "https://cinsscore.com/list/ci-badguys.txt",
                    "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
                    "https://reputation.alienvault.com/reputation.generic",
                    "https://www.blocklist.de/downloads/export-ips_all.txt",
                    "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
                    "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level2.netset"
                ],
                "urls": [
                    "https://urlhaus.abuse.ch/downloads/text_recent/",
                    "https://openphish.com/feed.txt",
                    "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt",
                    "https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list",
                    "https://raw.githubusercontent.com/mitchellkrogza/Suspicious.Snooping.Sniffing.Hacking.IP.Addresses/master/ips.list",
                    "https://phishing.army/download/phishing_army_blocklist_extended.txt",
                    "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-hosts.txt",
                    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
                ],
                "hashes": [
                    "https://bazaar.abuse.ch/export/txt/sha256/recent/",
                    "https://bazaar.abuse.ch/export/txt/md5/recent/",
                    "https://sslbl.abuse.ch/blacklist/sslblacklist.csv",
                    "https://raw.githubusercontent.com/Yara-Rules/rules/master/crypto/crypto_signatures.yar",
                    "https://bazaar.abuse.ch/export/txt/sha1/recent/",
                    "https://malshare.com/daily/malshare.current.txt",
                    "https://www.hybrid-analysis.com/feed?json"
                ]
            }
            logger.info("ThreatIntelCollector initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ThreatIntelCollector: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def fetch_feed(self, url, feed_name):
        retries = 3
        for attempt in range(retries):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                logger.info(f"Fetching {feed_name} from {url} (Attempt {attempt + 1}/{retries})")
                
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                lines = response.text.splitlines()
                logger.info(f"Successfully fetched {feed_name}: {len(lines)} lines")
                return lines
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout while fetching {feed_name} (Attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {feed_name} ({url}): {str(e)}")
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))
                    continue
                    
            except Exception as e:
                logger.error(f"Unexpected error fetching {feed_name}: {str(e)}")
                logger.error(traceback.format_exc())
                break
        
        return []

    def parse_c2_feed(self, lines):
        data = {
            "urls": set(),
            "ips": set(),
            "hashes": set()
        }
        
        for line in lines:
            if line and not line.startswith('#'):
                parts = line.strip().split(',')
                if len(parts) >= 1:
                    url = parts[0].strip().lower()
                    if url.startswith(('http://', 'https://')):
                        data["urls"].add(url)
                    
                    if len(parts) >= 2 and parts[1]:
                        ip = parts[1].strip()
                        try:
                            octets = ip.split('.')
                            if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                                data["ips"].add(ip)
                        except (ValueError, IndexError):
                            continue
                    
                    if len(parts) >= 3:
                        hash_value = parts[2].strip().lower()
                        if all(c in '0123456789abcdef' for c in hash_value):
                            if len(hash_value) in [32, 40, 64]:  # MD5, SHA1, or SHA256
                                data["hashes"].add(hash_value)
        
        return data

    def collect_feeds(self):
        try:
            all_data = {"ips": set(), "urls": set(), "hashes": set()}
            total_feeds = len(self.base_feeds["ips"]) + len(self.base_feeds["urls"]) + len(self.base_feeds["hashes"])
            successful_feeds = 0
            
            # Collect from C2 feeds
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_feed = {
                    executor.submit(self.fetch_feed, feed_url, feed_name): (feed_name, feed_url)
                    for feed_name, feed_url in self.c2_feeds.items()
                }
                
                for future in concurrent.futures.as_completed(future_to_feed):
                    feed_name, feed_url = future_to_feed[future]
                    try:
                        lines = future.result()
                        c2_data = self.parse_c2_feed(lines)
                        all_data["ips"].update(c2_data["ips"])
                        all_data["urls"].update(c2_data["urls"])
                        all_data["hashes"].update(c2_data["hashes"])
                        successful_feeds += 1
                    except Exception as e:
                        logger.error(f"Error processing {feed_name}: {e}")

            # Collect from base feeds
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for feed_type, urls in self.base_feeds.items():
                    future_to_url = {
                        executor.submit(self.fetch_feed, url, f"base-{feed_type}"): url
                        for url in urls
                    }
                    
                    for future in concurrent.futures.as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            lines = future.result()
                            if lines:
                                successful_feeds += 1
                                for line in lines:
                                    if line and not line.startswith('#'):
                                        all_data[feed_type].add(line.strip())
                        except Exception as e:
                            logger.error(f"Error processing {url}: {e}")
            
            success_rate = (successful_feeds / total_feeds) * 100 if total_feeds > 0 else 0
            logger.info(f"Feed collection complete. Success rate: {success_rate:.2f}%")
            
            if success_rate < 50:
                logger.warning("Less than 50% of feeds were successfully collected!")
            
            return all_data
        
        except Exception as e:
            logger.error(f"Error in collect_feeds: {str(e)}")
            logger.error(traceback.format_exc())
            return {"ips": set(), "urls": set(), "hashes": set()}

    def generate_feeds(self):
        try:
            logger.info("Starting feed generation...")
            all_data = self.collect_feeds()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
            
            for feed_type in ['ips', 'urls', 'hashes']:
                try:
                    filename = f"argonisintel_{feed_type.upper()}_Feed.txt"
                    logger.info(f"Writing {filename}...")
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"# Argonis Intel {feed_type.upper()} Feed\n")
                        f.write(f"# Generated: {timestamp}\n")
                        f.write(f"# Total: {len(all_data[feed_type])}\n")
                        f.write("# Feed Version: 2.2\n\n")
                        
                        for item in sorted(all_data[feed_type]):
                            f.write(f"{item}\n")
                    
                    logger.info(f"Successfully wrote {len(all_data[feed_type])} entries to {filename}")
                    
                except IOError as e:
                    logger.error(f"Error writing {filename}: {str(e)}")
                    continue
                    
            return {k: len(v) for k, v in all_data.items()}
        
        except Exception as e:
            logger.error(f"Error in generate_feeds: {str(e)}")
            logger.error(traceback.format_exc())
            return {"ips": 0, "urls": 0, "hashes": 0}

if __name__ == "__main__":
    try:
        logger.info("Starting threat intelligence collection...")
        collector = ThreatIntelCollector()
        stats = collector.generate_feeds()
        
        logger.info("\nCollection complete!")
        for feed_type, count in stats.items():
            logger.info(f"Generated {feed_type} feed with {count} entries")
        
        if sum(stats.values()) == 0:
            logger.error("No data was collected! Check the logs for errors.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Critical error in main execution: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
