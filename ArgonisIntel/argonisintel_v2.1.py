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
            "CobaltStrike-TPs": "https://threatview.io/Downloads/High-Confidence-CobaltStrike-C2%20-Feeds.txt",
            "unverified_c2_ips": "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/unverified/IPC2s.csv",
            "montysecurity_cs": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Cobalt%20Strike%20C2%20IPs.txt",
            "montysecurity_brute_ratel": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Brute%20Ratel%20C4%20IPs.txt",
            "montysecurity_sliver": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Sliver%20C2%20IPs.txt",
            "montysecurity_metasploit": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Metasploit%20Framework%20C2%20IPs.txt",
            "montysecurity_posh": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Posh%20C2%20IPs.txt",
            "montysecurity_havoc": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Havoc%20C2%20IPs.txt",
            "montysecurity_mythic": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Mythic%20C2%20IPs.txt",
            "montysecurity_burpsuite": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/BurpSuite%20IPs.txt",
            "montysecurity_deimos": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/Deimos%20C2%20IPs.txt",
            "montysecurity_nimplant": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/NimPlant%20C2%20IPs.txt",
            "montysecurity_panda": "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/PANDA%20C2%20IPs.txt",
            "threatmon_c2": "https://github.com/ThreatMon/ThreatMon-Daily-C2-Feeds"
        }
        
        # Base Feeds
        self.base_feeds = {
            "ips": [
                "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
                "https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt",
                "https://raw.githubusercontent.com/pan-unit42/iocs/master/known_good_ip.txt",
                "https://threatview.io/Downloads/IP-High-Confidence-Feed.txt",
                "https://lists.blocklist.de/lists/all.txt",
                "https://lists.blocklist.de/lists/ssh.txt",
                "https://lists.blocklist.de/lists/mail.txt",
                "https://lists.blocklist.de/lists/apache.txt",
                "https://lists.blocklist.de/lists/imap.txt",
                "https://lists.blocklist.de/lists/bots.txt",
                "https://lists.blocklist.de/lists/bruteforcelogin.txt",
                "https://lists.blocklist.de/lists/strongips.txt",
                "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
                "https://feodotracker.abuse.ch/blocklist/",
                "https://sslbl.abuse.ch/blacklist/sslipblacklist.txt",
                "https://sslbl.abuse.ch/blacklist/sslipblacklist_aggressive.txt",
                "http://reputation.alienvault.com/reputation.data",
                "http://www.talosintelligence.com/documents/ip-blacklist",
                "https://www.binarydefense.com/banlist.txt",
                "https://raw.githubusercontent.com/fox-it/cobaltstrike-extraneous-space/master/cobaltstrike-servers.csv",
                "https://iocfeed.mrlooquer.com/feed.csv",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/1.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/2.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/3.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/4.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/5.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/6.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/7.txt",
                "https://raw.githubusercontent.com/stamparm/ipsum/master/levels/8.txt",
                "https://raw.githubusercontent.com/montysecurity/C2-Tracker/main/data/all.txt",
                "https://snort.org/downloads/ip-block-list",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv",
                "https://rules.emergingthreats.net/blockrules/compromised-ips.txt",
                "https://reputation.alienvault.com/reputation.generic",
                "https://blocklist.greensnow.co/greensnow.txt",
                "https://cinsscore.com/list/ci-badguys.txt",
                "https://api.cybercure.ai/feed/get_ips?type=csv",
                "https://raw.githubusercontent.com/ktsaou/blocklist-ipsets/master/firehol_level1.netset",
                "https://mirai.security.gives/data/ip_list.txt",
                "https://cdn.ellio.tech/community-feed",
                "https://blocklists.0dave.ch/ssh.txt",
                "https://raw.githubusercontent.com/X4BNet/lists_vpn/main/output/vpn/ipv4.txt",
                "https://raw.githubusercontent.com/mthcht/awesome-lists/main/Lists/VPN/NordVPN/nordvpn_ips_list.csv",
                "https://raw.githubusercontent.com/mthcht/awesome-lists/main/Lists/VPN/ProtonVPN/protonvpn_ip_list.csv",
                "https://www.dan.me.uk/torlist/?exit",
                "https://www.dan.me.uk/torlist/?full",
                "https://www.spamhaus.org/drop/drop_v4.json"
            ],
            "urls": [
                "https://urlhaus.abuse.ch/downloads/text_recent/",
                "https://openphish.com/feed.txt",
                "https://raw.githubusercontent.com/stamparm/maltrail/master/trails/static/suspicious/malicious.txt",
                "https://threatview.io/Downloads/Experimental-IOC-Tweets.txt",
                "https://threatfox.abuse.ch/export/csv/urls/recent/",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv",
                "https://urlhaus.abuse.ch/downloads/csv_recent/",
                "https://phishing.army/download/phishing_army_blocklist.txt",
                "https://phishing.army/download/phishing_army_blocklist_extended.txt",
                "https://api.cybercure.ai/feed/get_url?type=csv",
                "https://openphish.com/feed.txt",
                "https://hole.cert.pl/domains/domains.csv",
                "https://threatview.io/Downloads/URL-High-Confidence-Feed.txt",
                "https://urlabuse.com/public/data/data.txt",
                "https://urlabuse.com/public/data/malware_url.txt",
                "https://urlabuse.com/public/data/phishing_url.txt",
                "https://urlabuse.com/public/data/hacked_url.txt",
                "https://osint.digitalside.it/Threat-Intel/lists/latesturls.txt",
		"https://threatfox.abuse.ch/downloads/hostfile/",
                "https://iocfeed.mrlooquer.com/feed.csv",
                "https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/blob/master/feeds/domainC2s.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv",
                "https://www.botvrij.eu/data/blocklist/blocklist_domain.csv",
                "https://trends.netcraft.com/cybercrime/tlds",
                "https://raw.githubusercontent.com/tsirolnik/spam-domains-list/master/spamdomains.txt",
                "https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt",
                "https://nocdn.nrd-list.com/0/nrd-list-32-days.txt",
                "https://nocdn.threat-list.com/0/domains.txt",
                "https://nocdn.threat-list.com/1/domains.txt",
                "https://threatview.io/Downloads/DOMAIN-High-Confidence-Feed.txt"
            ],
            "hashes": [
                "https://bazaar.abuse.ch/export/txt/sha256/recent/",
                "https://raw.githubusercontent.com/stamparm/maltrail/master/trails/static/suspicious/malicious.txt",
                "https://bazaar.abuse.ch/export/txt/md5/recent/",
                "https://threatfox.abuse.ch/export/csv/md5/recent/",
                "https://bazaar.abuse.ch/export/txt/sha1/recent/",
                "https://threatfox.abuse.ch/export/csv/sha256/recent/",
                "https://raw.githubusercontent.com/aptnotes/data/master/APTnotes.csv",
                "https://misp.cert.ssi.gouv.fr/feed-misp/hashes.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/week.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/month.csv",
                "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/year.csv",
                "https://api.cybercure.ai/feed/get_hash?type=csv",
                "https://www.botvrij.eu/data/ioclist.md5",
                "https://www.botvrij.eu/data/ioclist.sha256",
                "https://www.botvrij.eu/data/feed-osint/hashes.csv",
                "https://threatview.io/Downloads/MD5-HASH-ALL.txt",
                "https://threatview.io/Downloads/SHA-HASH-FEED.txt"
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
