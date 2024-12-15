import requests
import json
from datetime import datetime
from pathlib import Path
import time
import concurrent.futures

class ThreatIntelCollector:
    def __init__(self):
        self.data_dir = Path(".")
        
        # Updated C2 Intel Feeds URLs
        self.c2_feeds = {
            "c2_trackers": "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/C2_tracker.txt",
            "master_feed": "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/master-feed.txt",
            "CobaltStrike-TPs": "https://threatview.io/Downloads/High-Confidence-CobaltStrike-C2%20-Feeds.txt"
        }
        
        # Base Feeds
        self.base_feeds = {
            "ips": [
                "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
                "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt",
                "https://raw.githubusercontent.com/pan-unit42/iocs/master/known_good_ip.txt",
                "https://threatview.io/Downloads/IP-High-Confidence-Feed.txt"
            ],
            "urls": [
                "https://urlhaus.abuse.ch/downloads/text_recent/",
                "https://openphish.com/feed.txt",
                "https://raw.githubusercontent.com/stamparm/maltrail/master/trails/static/suspicious/malicious.txt",
                "https://threatview.io/Downloads/Experimental-IOC-Tweets.txt"
            ],
            "hashes": [
                "https://bazaar.abuse.ch/export/txt/sha256/recent/",
                "https://raw.githubusercontent.com/stamparm/maltrail/master/trails/static/suspicious/malicious.txt"
            ]
        }

    def fetch_feed(self, url, feed_name):
        """Fetch data from a feed URL with error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text.splitlines()
        except Exception as e:
            print(f"Error fetching {feed_name} ({url}): {e}")
            return []

    def parse_c2_feed(self, lines):
        """Parse C2 feed data"""
        data = {
            "urls": set(),
            "ips": set(),
            "hashes": set()
        }
        
        for line in lines:
            if line and not line.startswith('#'):
                parts = line.strip().split(',')
                if len(parts) >= 1:
                    # Clean and validate URL
                    url = parts[0].strip()
                    if url.startswith(('http://', 'https://')):
                        data["urls"].add(url)
                    
                    # Extract IP if present
                    if len(parts) >= 2 and parts[1]:
                        ip = parts[1].strip()
                        # Basic IP validation
                        if all(x.isdigit() and 0 <= int(x) <= 255 for x in ip.split('.')):
                            data["ips"].add(ip)
                    
                    # Extract hash if present
                    if len(parts) >= 3:
                        hash_value = parts[2].strip()
                        if len(hash_value) in [32, 40, 64]:  # MD5, SHA1, or SHA256
                            data["hashes"].add(hash_value)
        
        return data

    def collect_feeds(self):
        """Collect all feed data"""
        all_data = {
            "ips": set(),
            "urls": set(),
            "hashes": set()
        }
        
        # Collect from C2 feeds
        for feed_name, feed_url in self.c2_feeds.items():
            lines = self.fetch_feed(feed_url, feed_name)
            c2_data = self.parse_c2_feed(lines)
            all_data["ips"].update(c2_data["ips"])
            all_data["urls"].update(c2_data["urls"])
            all_data["hashes"].update(c2_data["hashes"])
        
        # Collect from base feeds
        for feed_type, urls in self.base_feeds.items():
            for url in urls:
                lines = self.fetch_feed(url, f"base-{feed_type}")
                for line in lines:
                    if line and not line.startswith('#'):
                        all_data[feed_type].add(line.strip())
        
        return all_data

    def generate_feeds(self):
        """Generate the three required feed files"""
        print("Collecting data from all sources...")
        all_data = self.collect_feeds()
        
        # Write IP feed
        print("Writing IP feed...")
        with open("argonisintel_IP_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel IP Feed\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"# Total IPs: {len(all_data['ips'])}\n\n")
            for ip in sorted(all_data["ips"]):
                f.write(f"{ip}\n")
        
        # Write URL feed
        print("Writing URL feed...")
        with open("argonisintel_URL_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel URL Feed\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"# Total URLs: {len(all_data['urls'])}\n\n")
            for url in sorted(all_data["urls"]):
                f.write(f"{url}\n")
        
        # Write Hash feed
        print("Writing Hash feed...")
        with open("argonisintel_Hash_Feed.txt", 'w', encoding='utf-8') as f:
            f.write("# Argonis Intel Hash Feed\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"# Total Hashes: {len(all_data['hashes'])}\n\n")
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