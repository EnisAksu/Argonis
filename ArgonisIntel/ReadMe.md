# Argonis Threat Intelligence Feeds

Argonis Threat Intelligence Feeds is an automated threat intelligence collection tool that aggregates and processes data from various reputable sources to provide up-to-date IP, URL, and hash-based indicators of compromise (IOCs).

## Features

- Automated collection of threat intelligence
- Three distinct feed types:
  - IP addresses
  - URLs
  - File hashes (MD5, SHA1, SHA256)
- Deduplication of indicators
- Automatic format standardization
- Parallel processing for efficient data collection
- Rate limiting to respect source feed restrictions
- Robust error handling

## Feed Sources

### Command and Control (C2) Intelligence
- [ThreatView CobaltStrike C2 Feed](https://threatview.io/)
  - *Attribution: High confidence CobaltStrike Command and Control server indicators*
- [Cybercrime Tracker](https://cybercrime-tracker.net/)
  - *Attribution: Tracking various cybercrime activities and C2 servers*

### IP Reputation Data
- [Stamparm/IPsum](https://github.com/stamparm/ipsum)
  - *Attribution: Daily updated IP reputation list of known malicious hosts*
- [Stamparm/Blackbook](https://github.com/stamparm/blackbook)
  - *Attribution: List of known malicious IP addresses*
- [Blocklist.de](https://www.blocklist.de/)
  - *Attribution: Various attack-based IP blocklists*
- [CI Army List](https://cinsscore.com/)
  - *Attribution: Collective Intelligence Network Security IP blocklist*
- [Feodo Tracker](https://feodotracker.abuse.ch/)
  - *Attribution: Tracking botnet C2 infrastructure*
- [AlienVault Reputation](https://reputation.alienvault.com/)
  - *Attribution: Community-driven IP reputation data*
- [FireHOL IP Lists](https://github.com/firehol/blocklist-ipsets)
  - *Attribution: Comprehensive IP blocklists for various threats*

### Malicious URL Sources
- [URLhaus by abuse.ch](https://urlhaus.abuse.ch/)
  - *Attribution: Collection of malware distribution URLs*
- [OpenPhish](https://openphish.com/)
  - *Attribution: Phishing URL feed using OpenPhish technology*
- [Mitchell Krogza's Phishing Database](https://github.com/mitchellkrogza/Phishing.Database)
  - *Attribution: Extensive collection of phishing URLs*
- [Malware Web Sites](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites)
  - *Attribution: Comprehensive list of compromised websites*
- [Phishing Army](https://phishing.army/)
  - *Attribution: Community-driven phishing URL blocklist*
- [Malware Filter](https://gitlab.com/malware-filter/urlhaus-filter)
  - *Attribution: Filtered and processed URLhaus data*
- [Steven Black Hosts](https://github.com/StevenBlack/hosts)
  - *Attribution: Unified hosts file with base extensions*

### Hash Intelligence
- [Malware Bazaar](https://bazaar.abuse.ch/)
  - *Attribution: Various hash types of recent malware samples*
- [SSL Blacklist](https://sslbl.abuse.ch/)
  - *Attribution: SSL certificate hashes associated with malicious activities*
- [YARA Rules Crypto](https://github.com/Yara-Rules/rules)
  - *Attribution: Cryptographic signatures for malware detection*
- [MalShare](https://malshare.com/)
  - *Attribution: Community-driven malware repository*
- [Hybrid Analysis](https://www.hybrid-analysis.com/)
  - *Attribution: Automated malware analysis service feed*

## Feed Formats

Each feed is provided in a simple text format with metadata headers:

```
# Argonis Intel [FEED_TYPE] Feed
# Generated: YYYY-MM-DD HH:MM:SS UTC
# Total [INDICATORS]: COUNT
# Feed Version: 2.2

[indicator entries - one per line]
```

## Usage

The script generates three distinct feed files:
- `argonisintel_IP_Feed.txt`
- `argonisintel_URL_Feed.txt`
- `argonisintel_Hash_Feed.txt`

To use the script:
1. Install the required dependencies:
```bash
pip install requests
```

2. Run the script:
```bash
python argonisintel_v2.py
```

## Implementation Details

- Concurrent processing using ThreadPoolExecutor
- Rate limiting with 2-second delays between requests
- Custom User-Agent headers for reliable data collection
- Enhanced validation for IPs, URLs, and hashes
- Robust error handling for network issues

## Disclaimer

These feeds are aggregated from public sources and should be used as additional data points in your security infrastructure. Always verify indicators before taking blocking actions.

## License

This project is open-source. However, please respect the licenses and attribution requirements of the original feed sources when using this data.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for:
- Additional feed sources
- Code improvements
- Bug fixes
- Documentation updates

---

*Note: This project is not affiliated with any of the source feed providers. All data is collected from publicly available sources.*