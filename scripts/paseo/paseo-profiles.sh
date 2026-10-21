#!/usr/bin/env bash
# Paseo の config.json に verifier プロファイルと、それが使う provider を反映する。
#
#   paseo-profiles.sh [--home DIR]
#
# --home の既定は $PASEO_HOME、未設定なら ~/.paseo。
# 定義は同じディレクトリの paseo-profiles.json。"requires" のコマンドが PATH に
# あるものだけを入れる (opencode が無い環境では opencode 系を入れない)。
# 置き換えるのは daemon.agentProfiles のうち id が "verifier-" で始まるものと、
# 利用可能な provider の定義だけ。それ以外のキーは変更しない。冪等。
# API キーは扱わない。
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SPEC="$SCRIPT_DIR/paseo-profiles.json"
HOME_DIR="${PASEO_HOME:-$HOME/.paseo}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --home)
      HOME_DIR="${2:?--home requires a directory}"
      shift 2
      ;;
    *)
      echo "usage: $0 [--home DIR]" >&2
      exit 2
      ;;
  esac
done

command -v jq >/dev/null 2>&1 || { echo "[paseo-profiles] jq is required" >&2; exit 1; }

CONFIG="$HOME_DIR/config.json"
mkdir -p -- "$HOME_DIR"
[[ -s "$CONFIG" ]] || echo '{}' >"$CONFIG"

available='[]'
while IFS= read -r cmd; do
  if command -v "$cmd" >/dev/null 2>&1; then
    available="$(jq -c --arg c "$cmd" '. + [$c]' <<<"$available")"
  else
    echo "[paseo-profiles] skip: '$cmd' not found" >&2
  fi
done < <(jq -r '[.providers[].requires, .profiles[].requires] | unique[]' "$SPEC")

tmp="$CONFIG.tmp.$$"
trap 'rm -f -- "$tmp"' EXIT
jq --slurpfile spec "$SPEC" --argjson avail "$available" '
  ($spec[0].profiles | map(select(.requires as $r | $avail | index($r)) | del(.requires))) as $profiles
  | ($spec[0].providers
      | with_entries(select(.value.requires as $r | $avail | index($r)) | .value |= del(.requires))) as $providers
  | .daemon.agentProfiles = (((.daemon.agentProfiles // []) | map(select(.id | startswith("verifier-") | not))) + $profiles)
  | .agents.providers = ((.agents.providers // {}) + $providers)
' "$CONFIG" >"$tmp"

if cmp -s -- "$tmp" "$CONFIG"; then
  echo "[paseo-profiles] no change: $CONFIG"
else
  mv -- "$tmp" "$CONFIG"
  echo "[paseo-profiles] updated: $CONFIG ($(jq -r '[.daemon.agentProfiles[].id | select(startswith("verifier-"))] | join(", ")' "$CONFIG"))"
  if command -v paseo >/dev/null 2>&1 \
    && [[ "$(paseo daemon status --home "$HOME_DIR" --json 2>/dev/null | jq -r '.localDaemon // empty')" == running ]]; then
    paseo daemon reload --home "$HOME_DIR" >/dev/null || echo "[paseo-profiles] WARNING: daemon reload failed" >&2
  fi
fi
