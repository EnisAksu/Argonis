# Argonis Threat Intelligence Feeds

Argonis Threat Intelligence Feeds is an automated threat intelligence collection tool that aggregates and processes data from various reputable sources to provide up-to-date IP, URL, and hash-based indicators of compromise (IOCs).

## Features

- Automated collection every 6 hours
- Three distinct feed types:
  - IP addresses
  - URLs
  - File hashes (MD5, SHA1, SHA256)
- Deduplication of indicators
- Automatic format standardization

## Feed Sources

### Command and Control (C2) Intelligence
- [drb-ra/C2IntelFeeds](https://github.com/drb-ra/C2IntelFeeds)
  - C2 Tracker Feed
  - Master Feed
  - *Attribution: These feeds provide command and control server information and associated indicators*

### IP Reputation Data
- [Stamparm/IPsum](https://github.com/stamparm/ipsum)
  - *Attribution: A daily updated IP reputation list of known malicious hosts*
- [Stamparm/Blackbook](https://github.com/stamparm/blackbook)
  - *Attribution: A list of known malicious IP addresses*
- [Palo Alto Unit42 IOCs](https://github.com/pan-unit42/iocs)
  - *Attribution: Known good IP addresses maintained by Palo Alto Networks Unit 42 team*

### Malicious URL Sources
- [URLhaus by abuse.ch](https://urlhaus.abuse.ch/)
  - *Attribution: A project by abuse.ch to collect and share malicious URLs used for malware distribution*
- [OpenPhish](https://openphish.com/)
  - *Attribution: A public feed of phishing URLs discovered using OpenPhish technology*
- [Maltrail Suspicious URLs](https://github.com/stamparm/maltrail)
  - *Attribution: Collection of suspicious and malicious URLs from the Maltrail project*

### Hash Intelligence
- [Bazaar by abuse.ch](https://bazaar.abuse.ch/)
  - *Attribution: Recent SHA256 hashes of malware samples*
- [Maltrail Suspicious Hashes](https://github.com/stamparm/maltrail)
  - *Attribution: Collection of suspicious and malicious file hashes from the Maltrail project*

## Feed Formats

Each feed is provided in a simple text format with metadata headers:

```
# Argonis Intel [FEED_TYPE] Feed
# Generated: YYYY-MM-DD HH:MM:SS UTC
# Total [INDICATORS]: COUNT

[indicator entries - one per line]
```

## Usage

The feeds are automatically updated every 6 hours and can be found in the following files:
- `ArgonisIntel/argonisintel_IP_Feed.txt`
- `ArgonisIntel/argonisintel_URL_Feed.txt`
- `ArgonisIntel/argonisintel_Hash_Feed.txt`

## Disclaimer

These feeds are aggregated from public sources and should be used as additional data points in your security infrastructure. Always verify indicators before taking blocking actions.

## License

Please respect the licenses and attribution requirements of the original feed sources when using this data.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for additional feeds or improvements.

---

*Note: This project is not affiliated with any of the source feed providers. All data is collected from publicly available sources.*
