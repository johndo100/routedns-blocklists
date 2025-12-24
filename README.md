# RouteDNS Blocklist (CI)

This repository **uses CI to convert upstream blocklist sources into RouteDNS-compatible domain lists** and **publishes the generated output publicly**.

The lists are built **for personal use**, based on my own needs and preferences.

## How It Works

- CI fetches upstream blocklists  
- Entries are normalized and filtered for DNS-level use  
- Domain-only lists are generated  
- Output files are published automatically  

## Sources

See [sources.toml](sources.toml).

Some blocklists you may find useful:

- [HaGeZi DNS Blocklists](https://github.com/hagezi/dns-blocklists)
- [StevenBlack Unified hosts](https://github.com/StevenBlack/hosts)
- [The Block List Project](https://github.com/blocklistproject/Lists)
- [oisd blocklist](https://github.com/sjhgvr/oisd)
- [1Hosts](https://github.com/badmojr/1Hosts)

## Notes

- Generated files are updated automatically via CI  
- False positives may occur  
- I already use some lists from [cbuijs](https://github.com/cbuijs), and this repository helps fill the gap  

## License

Provided as-is, without warranty.
