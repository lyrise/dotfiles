#!/usr/bin/env bash
set -euo pipefail
cd $(dirname $0)

SCRIPT_DIR="$(pwd)"

ln -s "$SCRIPT_DIR/agent/apm" "$HOME/.apm"
apm install -g

mkdir -p ~/.claude
mkdir -p ~/.codex

ln -sf "$SCRIPT_DIR/config/claude/CLAUDE.md" ~/.claude/CLAUDE.md
ln -sf "$SCRIPT_DIR/config/codex/AGENTS.md" ~/.codex/AGENTS.md
