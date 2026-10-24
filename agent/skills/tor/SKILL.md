---
name: tor
description: Search the web and fetch pages through the Tor SOCKS proxy (TOR_SOCKS_ADDR=tor:9050) with a stdlib-only Python CLI. Use when the user asks to search anonymously via Tor, find or open .onion (hidden service) sites, or fetch web content through Tor.
allowed-tools: Bash(python3 *tor.py:*) Bash(python3 -m py_compile:*)
---

# Tor Search & Fetch

A stdlib-only Python CLI that searches and fetches through the Tor SOCKS proxy. No dependency packages are required.

## Prerequisites

- tor runs as a resident service in a separate container, and SOCKS is reachable at `TOR_SOCKS_ADDR` (default `tor:9050`)
- DNS is also resolved on the tor side (SOCKS5 DOMAINNAME), so real `.onion` addresses are reachable
- GET only, no cookies sent. Do not use it for logins or form submissions

## Quick start

```bash
# Search (automatic fallback ddg → brave → torch)
python3 ~/.claude/skills/tor/scripts/tor.py search "query"

# Onion index search (torch is dedicated to finding .onion sites)
python3 ~/.claude/skills/tor/scripts/tor.py search "hidden wiki" --engine torch

# Fetch a page (.onion works too). --strip-html is recommended to make HTML readable
python3 ~/.claude/skills/tor/scripts/tor.py fetch "http://….onion/" --strip-html

# JSON for programmatic processing
python3 ~/.claude/skills/tor/scripts/tor.py search "query" --json --limit 5
```

## Commands

### search

```bash
tor.py search "query" [--engine auto|ddg|brave|torch] [--limit N] [--json]
```

- `--engine auto` (default): tries `ddg → brave → torch` in order, moving to the next on failure
- `--limit`: maximum number of results (default 10)

### fetch

```bash
tor.py fetch URL [--strip-html] [--max-bytes N] [--timeout SEC] [--json]
```

- Follows redirects and the `Onion-Location` header (which points to the onion version when tor is detected) automatically
- `--max-bytes`: limit on the body size fetched (default 200000 bytes; truncated when exceeded)
- The output header line shows `final_url / status / type / bytes [TRUNCATED]`

## Engine Cheat Sheet

| engine | Kind | Notes |
|---|---|---|
| `ddg` | General search | Often rejects tor exit IPs with 403. If it fails, leave it to auto |
| `brave` | General search | Independent index. May return 429 depending on the exit IP |
| `torch` | .onion index | Uncensored dark web engine. Ads are filtered |

## Cautions

- **ahmia currently requires JS** and is not supported (no non-JS version is implemented)
- 403 / 429 / timeouts depend on the tor exit IP. Retry after a while or switch the engine
- There is no ControlPort in this setup, so NEWNYM (forcing a new exit IP) is unavailable. Changing it requires editing the torrc in dockerfiles/paseo
- **torch results are uncensored**. Illegal or harmful ads and results may be mixed in; screen by title before opening a URL
- Do not forward fetched content or queries to third-party services (it breaks anonymity)
