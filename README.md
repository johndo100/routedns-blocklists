# RouteDNS Blocklists (Automation)

This repository uses **GitHub Actions automation** to convert upstream blocklist sources into **RouteDNS-compatible lists** and **publishes the generated output publicly as plain text files**.

The lists are built **for personal use**, based on my own needs and preferences, with a focus on **DNS-level blocking** and **Vietnamese-specific coverage**.

---

## How It Works

- GitHub Actions fetches upstream blocklist sources
- Entries are normalized for DNS-level use
- Unsupported formats are converted when required
- RouteDNS-compatible lists are generated
- Output files are updated and published automatically

All generated files are **auto-generated** and should be treated as **read-only**.

---

## Sources

Source definitions and conversion rules are documented in  
👉 **[`sources.toml`](sources.toml)**

### Input → RouteDNS Normalization

| Format            | Slug              | RouteDNS Type | Notes |
|-------------------|-------------------|---------------|-------|
| Domains           | domains           | domain        | Exact match only (e.g. `example.com`) |
| Hosts             | hosts             | hosts         | Standard hosts file format |
| Hosts (Compact)   | hosts-compact     | hosts         | Optimized hosts format |
| Adblock           | adblock           | —             | Adblock syntax (**conversion REQUIRED**) |
| DNSMasq           | dnsmasq           | —             | dnsmasq-style rules (**conversion REQUIRED**) |
| Wildcard (*)      | wildcard-asterisk | domain        | Subdomains only (e.g. `*.example.com`, root not matched) |
| Wildcard          | wildcard          | domain        | Root + subdomains (**MUST convert `example.com` → `.example.com`**) |
| RPZ               | rpz               | —             | Response Policy Zone format |

---

## Usage with RouteDNS

The generated blocklists are published as **plain text files** in the [`output`](output) directory and can be consumed directly by **RouteDNS** as external lists for either:

- **Query Blocklist**  
  https://github.com/folbricht/routedns/blob/master/doc/configuration.md#query-blocklist
- **Response Blocklist**  
  https://github.com/folbricht/routedns/blob/master/doc/configuration.md#response-blocklist

---

### Example: Using Blocklists

```toml
# Block queries (by name) using lists loaded from remote locations with HTTP and refreshed once a day
[groups.blocklist]
type = "blocklist-v2"
resolvers = ["blocklist-response"]
blocklist-refresh = 86400
blocklist-source = [
        {format = "domain", source = "https://raw.githubusercontent.com/cbuijs/hagezi/refs/heads/main/lists/multi/domains.routedns", allow-failure = true},
        {format = "hosts", source = "https://raw.githubusercontent.com/bigdargon/hostsVN/master/option/hosts-VN", allow-failure = true},
        {format = "hosts", source = "https://a.dove.isdumb.one/list.txt", allow-failure = true},
]

# Block responses that include certain names. Also loaded via HTTP and refreshed daily
[groups.blocklist-response]
type = "response-blocklist-name"
resolvers = ["blocklist-ip"]
blocklist-refresh = 86400
blocklist-source = [
        {format = "domain", source = "https://raw.githubusercontent.com/cbuijs/hagezi/refs/heads/main/lists/multi/domains.routedns", allow-failure = true},
        {format = "domain", source = "https://raw.githubusercontent.com/johndo100/routedns-blocklists/refs/heads/main/output/bigdargon-hostsvn-option-domain.routedns", allow-failure = true},
        {format = "domain", source = "https://raw.githubusercontent.com/johndo100/routedns-blocklists/refs/heads/main/output/a-dove-is-dumb-domain.routedns", allow-failure = true},
]
```

### Notes

- Use the **RouteDNS type** (`domain` or `hosts`) that matches the generated file  
- Files are **auto-updated**; RouteDNS will pick up changes on reload or restart  
- Lists are intended for **DNS-level blocking only** (no cosmetic or URL-path rules)  
- Multiple blocklists can be combined in a single listener or resolver  

---

## Related Blocklists

Some blocklist projects you may also find useful:

- [HaGeZi DNS Blocklists](https://github.com/hagezi/dns-blocklists)
- [StevenBlack Unified hosts](https://github.com/StevenBlack/hosts)
- [The Block List Project](https://github.com/blocklistproject/Lists)
- [oisd blocklist](https://github.com/sjhgvr/oisd)
- [1Hosts](https://github.com/badmojr/1Hosts)

---

## Notes

- Generated files are updated automatically via GitHub Actions
- False positives may occur
- I already use some lists from [cbuijs](https://github.com/cbuijs); this repository helps fill gaps, especially for Vietnamese-specific blocklists

---

## License

Provided **as-is**, without warranty.
