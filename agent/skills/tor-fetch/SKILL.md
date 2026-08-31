---
name: tor-fetch
description: Fetch web pages through the local Tor SOCKS proxy instead of the built-in webfetch tool. Use when the user explicitly asks for Tor or anonymous access, or the target URL is a .onion domain.
---

Fetch URLs through the local Tor daemon instead of the built-in webfetch tool. Use this skill only when the user explicitly requests Tor (e.g. "Torで", "anonymously") or the URL is a .onion domain. Do not use it for ordinary fetches.

## Prerequisites

- Tor daemon with SOCKS listening on 127.0.0.1:9050 (Tor default)
- `curl` and `html2text` (on Debian: `apt install html2text`)

## Procedure

1. Confirm the proxy actually reaches Tor before fetching anything:

   ```bash
   curl --socks5-hostname 127.0.0.1:9050 -s --max-time 30 https://check.torproject.org/api/ip
   ```

   Proceed only when the response contains `"IsTor":true`. If the check fails, tell the user the Tor daemon appears to be down and stop — never fall back to a direct (clearnet) fetch on your own.

2. Fetch the page and convert it to readable text:

   ```bash
   curl --socks5-hostname 127.0.0.1:9050 -sL --max-time 60 "<URL>" | html2text
   ```

   `--socks5-hostname` resolves DNS inside Tor as well. Keep the URL quoted.

## Notes

- When anonymity matters, report the exit IP from step 1 along with the fetched content.
- Never send credentials, cookies, or API keys through this path unless the user explicitly instructs it.
