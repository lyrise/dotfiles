---
name: tor-fetch
description: Search or fetch web pages through the local Tor SOCKS proxy. Use when the user explicitly asks for Tor or anonymous access, or the target URL is a .onion domain.
---

Search or fetch through the local Tor daemon instead of the built-in webfetch tool. Use this skill only when the user explicitly requests Tor (e.g. "Torで", "anonymously") or the URL is a .onion domain. Do not use it for ordinary searches or fetches.

## Prerequisites

- Tor daemon with SOCKS listening at `$TOR_SOCKS_ADDR` (default `127.0.0.1:9050`, the Tor default; in the paseo container it points to the compose tor service as `tor:9050`)
- `curl` and `html2text` (on Debian: `apt install html2text`)

## Procedure

1. Confirm the proxy actually reaches Tor before fetching anything:

   ```bash
   curl --socks5-hostname "${TOR_SOCKS_ADDR:-127.0.0.1:9050}" -s --max-time 30 https://check.torproject.org/api/ip
   ```

   Proceed only when the response contains `"IsTor":true`. If the check fails, tell the user the Tor daemon appears to be down and stop — never fall back to a direct (clearnet) fetch on your own, and never probe other proxy addresses on your own.

2. Fetch the page and convert it to readable text:

   ```bash
   curl --socks5-hostname "${TOR_SOCKS_ADDR:-127.0.0.1:9050}" -sL --max-time 60 "<URL>" | html2text
   ```

   `--socks5-hostname` resolves DNS inside Tor as well. Keep the URL quoted.

## Search through Tor

When the user gives search terms rather than a URL, use a search engine through the same SOCKS proxy after step 1. For general web searches, start with Brave Search's onion service. For searches specifically for `.onion` sites, use Ahmia. Honor a requested search engine. These are examples, not guaranteed endpoints:

| Engine | Search scope | Onion service | HTTPS site (also usable through Tor) |
| --- | --- | --- | --- |
| Brave Search | General web | `https://search.brave4u7jddbv7cyviptqjc7jusxh72uik7zt6adtckl5f4nwy2v72qd.onion/search` | `https://search.brave.com/search` |
| DuckDuckGo | General web | `https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/` | `https://duckduckgo.com/` |
| Ahmia | Public `.onion` sites | `http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/` | `https://ahmia.fi/` |

Build search requests with `curl -G --data-urlencode` so the terms are encoded rather than interpolated into the URL. For example:

```bash
curl --socks5-hostname "${TOR_SOCKS_ADDR:-127.0.0.1:9050}" -fsSL --max-time 60 \
  -G --data-urlencode "q=<search terms>" \
  "https://search.brave4u7jddbv7cyviptqjc7jusxh72uik7zt6adtckl5f4nwy2v72qd.onion/search" | html2text
```

Ahmia requires a rotating hidden field from its search form. Fetch its home page through Tor, read the current hidden input's name and value, then send both `q` and that field with `--data-urlencode` to `/search/` through Tor. Do not hard-code a previously observed field or token. Its onion service may be unavailable; its HTTPS site can still be reached through Tor.

Search providers may reject automated or Tor requests. Report the failure or try another listed endpoint through the verified SOCKS proxy; never retry directly. Verify the returned page contains actual search results before relying on it.

## Notes

- When anonymity matters, report the exit IP from step 1 along with the fetched content.
- Never send credentials, cookies, or API keys through this path unless the user explicitly instructs it.

Provider references: [Brave onion addresses](https://support.brave.com/hc/en-us/articles/4537609459469-List-of-Brave-Onion-Addresses), [DuckDuckGo onion service](https://support.torproject.org/tor-browser/features/default-search-engine/), [Ahmia and its official onion address](https://ahmia.fi/).
