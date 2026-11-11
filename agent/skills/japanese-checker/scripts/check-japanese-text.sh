#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "check-japanese-text: uv is required to run the bundled CLI" >&2
  exit 2
fi

skill_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
project_root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
project_wordlists="$project_root/.agents/skills/japanese-checker"

args=(
  --allow-words "$skill_dir/allow_words.txt"
  --deny-words "$skill_dir/deny_words.txt"
  --fix-words "$skill_dir/fix_words.txt"
)
for name in allow deny fix; do
  file="$project_wordlists/${name}_words.txt"
  if [[ -f "$file" ]]; then
    args+=("--${name}-words" "$file")
  fi
done

user_args=()
expect_value=0
for arg in "$@"; do
  if (( expect_value )); then
    user_args+=("$arg")
    expect_value=0
    continue
  fi
  case "$arg" in
    --allow-words | --deny-words | --fix-words)
      user_args+=("$arg")
      expect_value=1
      ;;
    --allow-words=* | --deny-words=* | --fix-words=*)
      user_args+=("$arg")
      ;;
    *)
      if [[ -d "$arg" ]]; then
        dir=$(cd -- "$arg" && pwd)
        found=0
        while IFS= read -r -d '' file; do
          user_args+=("$file")
          found=1
        done < <(
          find "$dir" \
            \( -path "$project_wordlists" -o -path "$skill_dir" \
               -o -name .git -o -name .venv -o -name node_modules -o -name .pytest_cache -o -name __pycache__ -o -name dist -o -name build \) -prune -o \
            -type f \( -name '*.txt' -o -name '*.md' \) -print0
        )
        if (( !found )); then
          echo "check-japanese-text: no .txt or .md files under $arg" >&2
          exit 2
        fi
      else
        user_args+=("$arg")
      fi
      ;;
  esac
done

exec uv run --project "$skill_dir/vendor/check-japanese-text" \
  check-japanese-text "${args[@]}" "${user_args[@]}"
