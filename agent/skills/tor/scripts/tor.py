#!/usr/bin/env python3
"""Search and fetch via the Tor SOCKS proxy, using only the Python standard library.

Usage:
  tor.py search "query" [--engine auto|ddg|brave|ahmia|torch] [--limit N] [--json]
  tor.py fetch URL [--max-bytes N] [--strip-html] [--json] [--timeout SEC]
"""

import argparse
import http.client
import json
import os
import re
import socket
import ssl
import sys
from html import unescape
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

DEFAULT_PROXY = os.environ.get("TOR_SOCKS_ADDR", "tor:9050")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
)
MAX_REDIRECTS = 5
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_BYTES = 200_000

TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_STYLE_RE = re.compile(
    r"<(script|style|noscript)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL
)
ANCHOR_RE = re.compile(r"<a\s([^>]*)>(.*?)</a>", re.DOTALL | re.IGNORECASE)
HREF_RE = re.compile(r"""href=(?:"([^"]*)"|'([^']*)'|(\S+))""", re.IGNORECASE)

TORCH_HOST = "torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion"
TORCH_AD_HOSTS = ("tordexu73joywapk2txdr54jed4imqledpcvcuf75qsas2gwdgksvnyd.onion",)


class TorError(Exception):
    pass


class ProxyRefused(TorError):
    pass


def parse_proxy(spec):
    host, sep, port = spec.rpartition(":")
    if not sep:
        raise TorError(f"invalid TOR_SOCKS_ADDR: {spec!r} (expected host:port)")
    return host, int(port)


def socks5_connect(proxy, dst_host, dst_port, timeout):
    host, port = proxy
    raw = socket.create_connection((host, port), timeout=timeout)
    try:
        raw.settimeout(timeout)
        raw.sendall(b"\x05\x01\x00")
        resp = raw.recv(2)
        if resp != b"\x05\x00":
            raise ProxyRefused(f"SOCKS5 handshake failed: {resp!r}")
        try:
            addr = dst_host.encode("ascii")
        except UnicodeEncodeError:
            addr = dst_host.encode("idna")
        if len(addr) > 255:
            raise TorError(f"hostname too long: {dst_host}")
        raw.sendall(
            b"\x05\x01\x00\x03" + bytes([len(addr)]) + addr + dst_port.to_bytes(2, "big")
        )
        resp = raw.recv(4)
        if len(resp) < 4:
            raise ProxyRefused("SOCKS5 connect: short reply")
        if resp[1] != 0x00:
            reasons = {
                1: "general failure",
                2: "not allowed",
                3: "network unreachable",
                4: "host unreachable",
                5: "connection refused",
                6: "TTL expired",
                7: "command not supported",
                8: "address type not supported",
            }
            raise ProxyRefused(
                f"SOCKS5 connect failed: {resp[1]} ({reasons.get(resp[1], '?')}) "
                f"for {dst_host}:{dst_port}"
            )
        atyp = resp[3]
        if atyp == 0x01:
            raw.recv(4 + 2)
        elif atyp == 0x03:
            n = raw.recv(1)[0]
            raw.recv(n + 2)
        elif atyp == 0x04:
            raw.recv(16 + 2)
        else:
            raise ProxyRefused(f"unknown SOCKS5 address type: {atyp}")
        return raw
    except Exception:
        raw.close()
        raise


class TorHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host, port, proxy, timeout):
        super().__init__(host, port, timeout=timeout)
        self._proxy = proxy

    def connect(self):
        self.sock = socks5_connect(self._proxy, self.host, self.port, self.timeout)


class TorHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, port, proxy, timeout):
        super().__init__(host, port, timeout=timeout)
        self._proxy = proxy
        self._ctx = ssl.create_default_context()

    def connect(self):
        raw = socks5_connect(self._proxy, self.host, self.port, self.timeout)
        self.sock = self._ctx.wrap_socket(raw, server_hostname=self.host)


def request(url, timeout=DEFAULT_TIMEOUT, max_bytes=DEFAULT_MAX_BYTES):
    """GET url through Tor; follow redirects.

    Returns (final_url, status, headers, body_bytes, truncated).
    """
    proxy = parse_proxy(DEFAULT_PROXY)
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        parts = urlsplit(current)
        if parts.scheme not in ("http", "https"):
            raise TorError(f"unsupported scheme: {parts.scheme!r} in {current}")
        if not parts.hostname:
            raise TorError(f"no hostname in URL: {current}")
        port = parts.port or (443 if parts.scheme == "https" else 80)
        cls = TorHTTPSConnection if parts.scheme == "https" else TorHTTPConnection
        conn = cls(parts.hostname, port, proxy, timeout)
        path = parts.path or "/"
        if parts.query:
            path += "?" + parts.query
        try:
            conn.request(
                "GET",
                path,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.8,ja;q=0.6",
                    "Connection": "close",
                },
            )
            resp = conn.getresponse()
            body = resp.read(max_bytes + 1)
            truncated = len(body) > max_bytes
            if truncated:
                body = body[:max_bytes]
            status = resp.status
            headers = dict(resp.getheaders())
        finally:
            conn.close()
        if status in (301, 302, 303, 307, 308) and headers.get("location"):
            current = urljoin(current, headers["location"])
            continue
        onion_loc = headers.get("onion-location")
        if onion_loc and ".onion" in onion_loc and ".onion" not in current:
            current = urljoin(current, onion_loc)
            continue
        return current, status, headers, body, truncated
    raise TorError(f"too many redirects fetching {url}")


def decode_body(body, content_type):
    m = re.search(r"charset=([\w\-]+)", content_type or "", re.IGNORECASE)
    for enc in ([m.group(1)] if m else []) + ["utf-8", "latin-1"]:
        try:
            return body.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return body.decode("utf-8", errors="replace")


def strip_html(data, content_type="text/html"):
    text = decode_body(data, content_type) if isinstance(data, bytes) else data
    text = SCRIPT_STYLE_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = unescape(text)
    return re.sub(r"[ \t]+", " ", text).strip()


def clean_text(s):
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub("", s))).strip()


def parse_links(html_text, base_url, class_filter=None):
    """Yield (href, attrs, title) for each <a> tag in document order."""
    for m in ANCHOR_RE.finditer(html_text):
        attrs = m.group(1)
        href_m = HREF_RE.search(attrs)
        if not href_m:
            continue
        href = href_m.group(1) or href_m.group(2) or href_m.group(3) or ""
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        if class_filter and class_filter not in attrs:
            continue
        yield urljoin(base_url, href), attrs, clean_text(m.group(2))


# --- engines -----------------------------------------------------------------


def extract_ddg_href(href):
    """DDG wraps results in a redirect: //duckduckgo.com/l/?uddg=<enc>&rut=..."""
    if "uddg=" in href:
        return parse_qs(urlsplit(href).query).get("uddg", [href])[0]
    return href


def search_ddg(query, limit):
    url = "https://html.duckduckgo.com/html/?" + urlencode({"q": query})
    final_url, status, headers, body, _ = request(url)
    if status != 200:
        raise TorError(f"ddg returned HTTP {status}")
    text = decode_body(body, headers.get("content-type"))
    results = []
    seen = set()
    for href, _attrs, title in parse_links(text, final_url, class_filter="result__a"):
        real = extract_ddg_href(href)
        if "duckduckgo.com/y.js" in real:  # ad link
            continue
        if real in seen or not title:
            continue
        seen.add(real)
        results.append({"title": title, "url": real, "snippet": ""})
        if len(results) >= limit:
            break
    snips = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', text, re.DOTALL)
    for i, s in enumerate(snips[: len(results)]):
        results[i]["snippet"] = clean_text(s)
    if not results:
        raise TorError("ddg returned no results")
    return results


def search_brave(query, limit):
    url = "https://search.brave.com/search?" + urlencode({"q": query})
    final_url, status, headers, body, _ = request(url)
    if status != 200:
        raise TorError(f"brave returned HTTP {status}")
    text = decode_body(body, headers.get("content-type"))
    results = []
    seen = set()
    skip = ("brave.com", "safesearch", "h.mozilla.org", "support.mozilla.org")
    for href, _attrs, title in parse_links(text, final_url):
        if not title or len(title) < 2:
            continue
        p = urlsplit(href)
        if p.scheme not in ("http", "https"):
            continue
        if any(s in href for s in skip):
            continue
        if href in seen:
            continue
        seen.add(href)
        results.append({"title": title, "url": href, "snippet": ""})
        if len(results) >= limit:
            break
    if not results:
        raise TorError("brave returned no results")
    return results


def search_torch(query, limit):
    url = f"http://{TORCH_HOST}/search?" + urlencode({"query": query})
    final_url, status, headers, body, _ = request(url)
    if status != 200:
        raise TorError(f"torch returned HTTP {status}")
    text = decode_body(body, headers.get("content-type"))
    results = []
    seen = set()
    for href, _attrs, title in parse_links(text, final_url):
        if not title or TORCH_HOST in href:
            continue
        if any(ad in href for ad in TORCH_AD_HOSTS) or "kads=" in href or "bads=" in href:
            continue  # ad banner
        if urlsplit(href).scheme not in ("http", "https"):
            continue
        if href in seen or title.startswith("http"):
            continue  # duplicate entry whose title is the bare URL
        seen.add(href)
        results.append({"title": title, "url": href, "snippet": ""})
        if len(results) >= limit:
            break
    if not results:
        raise TorError("torch returned no results")
    return results


ENGINES = {
    "ddg": search_ddg,
    "brave": search_brave,
    "torch": search_torch,
}
FALLBACK_CHAIN = ["ddg", "brave", "torch"]


def do_search(args):
    chain = FALLBACK_CHAIN if args.engine == "auto" else [args.engine]
    errors = []
    for engine in chain:
        try:
            return engine, ENGINES[engine](args.query, max(1, args.limit))
        except Exception as e:
            errors.append(f"{engine}: {e}")
    raise TorError("all engines failed:\n  " + "\n  ".join(errors))


def cmd_search(args):
    engine, results = do_search(args)
    if args.as_json:
        print(
            json.dumps(
                {"engine": engine, "query": args.query, "results": results},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        lines = [f"engine: {engine}  query: {args.query!r}  results: {len(results)}", ""]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   {r['url']}")
            if r["snippet"]:
                lines.append(f"   {r['snippet'][:200]}")
        print("\n".join(lines))


def do_fetch(args):
    final_url, status, headers, body, truncated = request(
        args.url, timeout=args.timeout, max_bytes=args.max_bytes
    )
    ctype = headers.get("content-type", "")
    head = body[:512].lstrip().lower()
    is_html = "html" in ctype.lower() or (
        not ctype and (head.startswith(b"<!doctype") or head.startswith(b"<html"))
    )
    if args.strip_html and is_html:
        content = strip_html(body, ctype)
    else:
        content = decode_body(body, ctype)
    if args.as_json:
        print(
            json.dumps(
                {
                    "requested_url": args.url,
                    "final_url": final_url,
                    "status": status,
                    "content_type": ctype,
                    "truncated": truncated,
                    "length": len(body),
                    "body": content,
                },
                ensure_ascii=False,
            )
        )
    else:
        note = " [TRUNCATED]" if truncated else ""
        print(
            f"url: {final_url}\nstatus: {status}  type: {ctype}  "
            f"bytes: {len(body)}{note}\n{'-' * 60}"
        )
        sys.stdout.write(content)
        if not content.endswith("\n"):
            print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tor.py", description="Search and fetch via Tor SOCKS proxy (stdlib only)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="search the web through Tor")
    p_search.add_argument("query")
    p_search.add_argument(
        "--engine",
        choices=["auto", "ddg", "brave", "torch"],
        default="auto",
        help="search engine (auto = ddg -> brave -> torch fallback)",
    )
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--json", action="store_true", dest="as_json")
    p_search.set_defaults(func=cmd_search)

    p_fetch = sub.add_parser("fetch", help="fetch a URL through Tor")
    p_fetch.add_argument("url")
    p_fetch.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    p_fetch.add_argument(
        "--strip-html", action="store_true", help="remove HTML tags (HTML pages only)"
    )
    p_fetch.add_argument("--json", action="store_true", dest="as_json")
    p_fetch.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p_fetch.set_defaults(func=do_fetch)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except TorError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except (socket.timeout, TimeoutError):
        print(
            f"error: timed out (Tor can be slow; try --timeout {DEFAULT_TIMEOUT * 2})",
            file=sys.stderr,
        )
        return 2
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
