---
name: tor
description: Search the web and fetch pages through the Tor SOCKS proxy (TOR_SOCKS_ADDR=tor:9050) with a stdlib-only Python CLI. Use when the user asks to search anonymously via Tor, find or open .onion (hidden service) sites, or fetch web content through Tor.
allowed-tools: Bash(python3 *tor.py:*) Bash(python3 -m py_compile:*)
---

# Tor Search & Fetch

Tor SOCKS プロキシ経由で検索・取得を行う標準ライブラリのみの Python CLI。依存パッケージ不要。

## 前提

- tor は別コンテナで常駐し、SOCKS は `TOR_SOCKS_ADDR`(既定 `tor:9050`)で到達可能
- DNS も tor 側で解決される(SOCKS5 DOMAINNAME)。本物の `.onion` 到達が可能
- GET のみ・cookie 送信なし。ログインやフォーム送信には使わないこと

## Quick start

```bash
# 検索(ddg → brave → torch の自動フォールバック)
python3 ~/.claude/skills/tor/scripts/tor.py search "query"

# onion インデックス検索(torch は .onion サイトを探す専用)
python3 ~/.claude/skills/tor/scripts/tor.py search "hidden wiki" --engine torch

# ページ取得(.onion も可)。HTML を読みやすくする --strip-html 推奨
python3 ~/.claude/skills/tor/scripts/tor.py fetch "http://….onion/" --strip-html

# プログラム処理向け JSON
python3 ~/.claude/skills/tor/scripts/tor.py search "query" --json --limit 5
```

## Commands

### search

```bash
tor.py search "query" [--engine auto|ddg|brave|torch] [--limit N] [--json]
```

- `--engine auto`(既定): `ddg → brave → torch` の順に試し、失敗したら次へ
- `--limit`: 最大結果数(既定 10)

### fetch

```bash
tor.py fetch URL [--strip-html] [--max-bytes N] [--timeout SEC] [--json]
```

- リダイレクトと `Onion-Location` ヘッダ(tor 検知時に onion 版へ誘導)を自動追従
- `--max-bytes`: 本文の取得上限(既定 200000 バイト、超過時は切り詰め表示)
- 出力ヘッダ行に `final_url / status / type / bytes [TRUNCATED]` を表示

## エンジン早見表

| engine | 種類 | 補足 |
|---|---|---|
| `ddg` | 一般検索 | tor 出口 IP を 403 で弾くことが多い。だめなら auto に任せる |
| `brave` | 一般検索 | 独立インデックス。出口 IP により 429 が出ることがある |
| `torch` | .onion インデックス | 検閲なしの dark web エンジン。広告はフィルタ済み |

## 注意

- **ahmia は現在 JS 必須**のため非対応(非 JS 版が実装されていない)
- 403 / 429 / タイムアウトは tor 出口 IP 依存。時間を置いて再実行するか engine を変える
- ControlPort が無い構成のため NEWNYM(出口 IP 強制切替)は不可。変えたい場合は dockerfiles/paseo の torrc 変更が必要
- **torch の結果は無検閲**。違法・有害な広告や結果が混ざりうる点に注意し、URL を開く前にタイトルで選別すること
- 取得した内容やクエリを第三者サービスに転送しない(匿名性が崩れる)
