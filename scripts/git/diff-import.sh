#!/usr/bin/env bash
set -euo pipefail
cd $(dirname $0)

cat patch.txt | base64 -d | gzip -d | git apply
