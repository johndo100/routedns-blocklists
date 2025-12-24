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

| Format            | Slug              | RouteDNS Type | Notes                                                                      |
|-------------------|-------------------|---------------|----------------------------------------------------------------------------|
| Domains           | domains           | domain        | Exact match only (e.g. `example.com`)                                       |
| Hosts             | hosts             | hosts         | Standard hosts file format                                                  |
| Hosts (Compact)   | hosts-compact     | hosts         | Optimized hosts format                                                      |
| Adblock           | adblock           | —             | Adblock syntax (**conversion REQUIRED**)                                    |
| DNSMasq           | dnsmasq           | —             | dnsmasq-style rules (**conversion REQUIRED**)                               |
| Wildcard (*)      | wildcard-asterisk | domain        | Subdomains only (e.g. `*.example.com`, root NOT matched)                    |
| Wildcard          | wildcard          | domain        | Root + subdomains (**MUST convert `example.com` → `.example.com`**)        |
| RPZ               | rpz               | —             | Response Policy Zone format                                                 |

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
