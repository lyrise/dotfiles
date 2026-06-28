#!/usr/bin/env bash
set -euo pipefail
cd $(dirname $0)

git diff --diff-filter=AMCRD HEAD | gzip -c | base64 > patch.txt
