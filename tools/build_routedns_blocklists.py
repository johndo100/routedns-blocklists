#!/usr/bin/env python3

import tomllib
import requests
from pathlib import Path
from datetime import datetime, timezone

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT_DIR / "sources.toml"
OUTPUT_DIR = ROOT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def normalize_domain(domain: str) -> str:
    return domain.strip().lower().rstrip(".")


def parse_domains(lines):
    """
    Parse plain domain lists.
    Deduplicated via set + normalization.
    """
    out = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.add(normalize_domain(line))
    return out


def hosts_to_domain(lines):
    """
    Convert hosts-style entries to wildcard domains.

    0.0.0.0 example.com  ->  .example.com
    :: example.com       ->  .example.com
    """
    out = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        domain = normalize_domain(parts[1])
        if domain and domain not in ("localhost", "localhost.localdomain"):
            out.add("." + domain)

    return out


def prepend_dot(domains):
    """
    example.com -> .example.com
    """
    return {"." + normalize_domain(d) for d in domains if d}


def dedupe_hosts(lines):
    """
    Deduplicate hosts entries by domain.
    Keeps the first occurrence only.

    0.0.0.0 example.com
    127.0.0.1 example.com   -> keep first
    """
    out = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        ip = parts[0]
        domain = normalize_domain(parts[1])

        if domain not in out:
            out[domain] = f"{ip} {domain}"

    return set(out.values())

def normalize_filename(s: str) -> str:
    return s.strip().lower()

# --------------------------------------------------
# Core processing
# --------------------------------------------------

def process_source(src):
    name = src["name"]
    input_format = src["input_format"]
    output_format = src["output_format"]
    conversion = src.get("conversion", False)
    rule = src.get("conversion_rule")

    print(f"[+] {name}: {input_format} → {output_format}")

    resp = requests.get(src["url"], timeout=30)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    data = set()

    # ---- Input parsing ----
    if input_format == "domains":
        data = parse_domains(lines)

    elif input_format == "hosts":
        if conversion and rule == "hosts-to-domain":
            data = hosts_to_domain(lines)
        else:
            data = dedupe_hosts(lines)

    else:
        raise ValueError(f"Unsupported input_format: {input_format}")

    # ---- Post conversion ----
    if conversion and output_format == "domain":
        if rule == "prepend-dot":
            data = prepend_dot(data)
        elif rule == "hosts-to-domain":
            pass  # already handled
        else:
            raise ValueError(f"Unknown conversion_rule: {rule}")

    # ---- Write output ----
    filename = normalize_filename(f"{name}-{output_format}.routedns")
    out_file = OUTPUT_DIR / filename

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry_count = len(data)

    with out_file.open("w") as f:
        f.write(f"# Title: {name}\n")
        f.write(f"# Source: {src['url']}\n")
        f.write(f"# Last modified: {now_utc}\n")
        f.write(f"# Syntax: {output_format}\n")
        f.write(f"# Number of entries: {entry_count}\n")
        f.write("#\n")

        for item in sorted(data):
            f.write(item + "\n")

    print(f"    → output/{out_file.name} ({entry_count} entries)")


def main():
    with SOURCES_FILE.open("rb") as f:
        config = tomllib.load(f)

    for src in config.get("source", []):
        process_source(src)


if __name__ == "__main__":
    main()
