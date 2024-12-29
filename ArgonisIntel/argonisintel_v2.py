import requests
import json
from datetime import datetime
from pathlib import Path
import time
import concurrent.futures

class ThreatIntelCollector:
    def __init__(self):
        # Get the repository root directory (where the script is running from)
        self.repo_root = Path(__file__).parent.parent
        # Create the output directory if it doesn't exist
        self.data_dir = Path("ArgonisIntel")
        self.data_dir.mkdir(exist_ok=True)
        
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

    def fetch_feed(self, url, feed_name):
        """Fetch data from a feed URL with error handling and rate limiting"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Add delay to prevent rate limiting
            time.sleep(2)
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text.splitlines()
        except Exception as e:
            print(f"Error fetching {feed_name} ({url}): {e}")
            return []

    def parse_c2_feed(self, lines):
        """Parse C2 feed data with enhanced validation"""
        data = {
            "urls": set(),
            "ips": set(),
            "hashes": set()
        }
        
        for line in lines:
            if line and not line.startswith('#'):
                parts = line.strip().split(',')
                if len(parts) >= 1:
                    # Enhanced URL validation
                    url = parts[0].strip().lower()
                    if url.startswith(('http://', 'https://')):
                        data["urls"].add(url)
                    
                    # Enhanced IP validation
                    if len(parts) >= 2 and parts[1]:
                        ip = parts[1].strip()
                        try:
                            octets = ip.split('.')
                            if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                                data["ips"].add(ip)
                        except (ValueError, IndexError):
                            continue
                    
                    # Enhanced hash validation
                    if len(parts) >= 3:
                        hash_value = parts[2].strip().lower()
                        if all(c in '0123456789abcdef' for c in hash_value):
                            if len(hash_value) in [32, 40, 64]:  # MD5, SHA1, or SHA256
                                data["hashes"].add(hash_value)
        
        return data

    def collect_feeds(self):
        """Collect all feed data with parallel processing"""
        all_data = {
            "ips": set(),
            "urls": set(),
            "hashes": set()
        }
        
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
                except Exception as e:
                    print(f"Error processing {feed_name}: {e}")
        
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
                        for line in lines:
                            if line and not line.startswith('#'):
                                all_data[feed_type].add(line.strip())
                    except Exception as e:
                        print(f"Error processing {url}: {e}")
        
        return all_data

    def generate_feeds(self):
        """Generate the three required feed files with enhanced metadata"""
        print("Collecting data from all sources...")
        all_data = self.collect_feeds()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Write IP feed
        print("Writing IP feed...")
        with open("argonisintel_IP_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel IP Feed\n")
            f.write(f"# Generated: {timestamp}\n")
            f.write(f"# Total IPs: {len(all_data['ips'])}\n")
            f.write("# Feed Version: 2.2\n\n")
            for ip in sorted(all_data["ips"]):
                f.write(f"{ip}\n")
        
        # Write URL feed
        print("Writing URL feed...")
        with open("argonisintel_URL_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel URL Feed\n")
            f.write(f"# Generated: {timestamp}\n")
            f.write(f"# Total URLs: {len(all_data['urls'])}\n")
            f.write("# Feed Version: 2.2\n\n")
            for url in sorted(all_data["urls"]):
                f.write(f"{url}\n")
        
        # Write Hash feed
        print("Writing Hash feed...")
        with open("argonisintel_Hash_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel Hash Feed\n")
            f.write(f"# Generated: {timestamp}\n")
            f.write(f"# Total Hashes: {len(all_data['hashes'])}\n")
            f.write("# Feed Version: 2.2\n\n")
            for hash_value in sorted(all_data["hashes"]):
                f.write(f"{hash_value}\n")
        
        return {
            "ips": len(all_data["ips"]),
            "urls": len(all_data["urls"]),
            "hashes": len(all_data["hashes"])
        }

if __name__ == "__main__":
    collector = ThreatIntelCollector()
    
    print("Starting threat intelligence collection...")
    stats = collector.generate_feeds()
    
    print("\nCollection complete!")
    print(f"Generated argonisintel_IP_Feed.txt with {stats['ips']} IPs")
    print(f"Generated argonisintel_URL_Feed.txt with {stats['urls']} URLs")
    print(f"Generated argonisintel_Hash_Feed.txt with {stats['hashes']} hashes")