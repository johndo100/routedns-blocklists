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

## Notes

- Generated files are updated automatically via CI
- False positives may occur
- I use some lists from [cbuijs](https://github.com/cbuijs), and this repository fills the gaps based on my needs.

## License

Provided as-is, without warranty.
