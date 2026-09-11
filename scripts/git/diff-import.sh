#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
repo_root=$(git -C "$script_dir" rev-parse --show-toplevel)
patch_file="$script_dir/patch.txt"

if [[ ! -r "$patch_file" ]]; then
  printf 'patch file is not readable: %s\n' "$patch_file" >&2
  exit 1
fi

decoded_patch=$(mktemp)
trap 'rm -f "$decoded_patch"' EXIT
base64 -d < "$patch_file" | gzip -dc > "$decoded_patch"

printf 'Applying %s to %s:\n' "$patch_file" "$repo_root"
git -C "$repo_root" apply --stat < "$decoded_patch"
git -C "$repo_root" apply --check < "$decoded_patch"
git -C "$repo_root" apply < "$decoded_patch"
printf 'Applied patch to %s\n' "$repo_root"
