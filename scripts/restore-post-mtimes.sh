#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
posts_dir="${1:-content/posts}"

cd "$repo_root"

if [[ ! -d "$posts_dir" ]]; then
  echo "Posts directory not found: $posts_dir" >&2
  exit 1
fi

has_gnu_touch=false
if touch --version >/dev/null 2>&1; then
  has_gnu_touch=true
fi

has_gtouch=false
if command -v gtouch >/dev/null 2>&1; then
  has_gtouch=true
fi

to_bsd_touch_timestamp() {
  local iso="$1"
  local normalized

  normalized="${iso/Z/+0000}"
  normalized="$(printf '%s' "$normalized" | sed -E 's/\.[0-9]+//; s/([+-][0-9]{2}):([0-9]{2})/\1\2/')"

  date -j -f "%Y-%m-%dT%H:%M:%S%z" "$normalized" "+%Y%m%d%H%M.%S"
}

restored=0
skipped=0

while IFS= read -r -d '' file; do
  ts="$(git log -1 --format=%cI -- "$file" || true)"
  if [[ -z "$ts" ]]; then
    skipped=$((skipped + 1))
    continue
  fi

  if [[ "$has_gtouch" == true ]]; then
    gtouch -d "$ts" "$file"
  elif [[ "$has_gnu_touch" == true ]]; then
    touch -d "$ts" "$file"
  else
    touch -t "$(to_bsd_touch_timestamp "$ts")" "$file"
  fi

  restored=$((restored + 1))
done < <(find "$posts_dir" -type f -name '*.md' -print0)

echo "Restored mtimes for $restored files (skipped $skipped)."
