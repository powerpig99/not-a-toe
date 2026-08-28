#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT/notebooklm-auto"

SLUG="$1"

if [ -z "$SLUG" ]; then
    echo "Usage: ./scripts/generate-podcast.sh <slug-or-url-or-markdown-path> [--text]"
    echo "Example (URL Mode - Default): ./scripts/generate-podcast.sh cong-xing-shi-mi-si-dao-luo-ji-bi-huan"
    echo "Example (Direct URL):         ./scripts/generate-podcast.sh https://powerpig99.github.io/not-a-toe/posts/cong-xing-shi-mi-si-dao-luo-ji-bi-huan/"
    echo "Example (Local File Mode):    ./scripts/generate-podcast.sh content/posts/cong-xing-shi-mi-si-dao-luo-ji-bi-huan.md"
    exit 1
fi

MODE_FLAG="$2"
LIVE_BASE_URL="https://powerpig99.github.io/not-a-toe/posts"

if [[ "$SLUG" == http://* ]] || [[ "$SLUG" == https://* ]]; then
    TARGET_INPUT="$SLUG"
    BASENAME="$(echo "$SLUG" | sed 's:/*$::' | awk -F/ '{print $NF}')"
elif [ "$MODE_FLAG" == "--text" ] && [ -f "$REPO_ROOT/content/posts/${SLUG}.md" ]; then
    TARGET_INPUT="$REPO_ROOT/content/posts/${SLUG}.md"
    BASENAME="$SLUG"
elif [ -f "$SLUG" ]; then
    TARGET_INPUT="$SLUG"
    BASENAME="$(basename "$SLUG" .md)"
else
    # Default: Use published live blog URL
    CLEAN_SLUG="$(basename "$SLUG" .md)"
    TARGET_INPUT="${LIVE_BASE_URL}/${CLEAN_SLUG}/"
    BASENAME="$CLEAN_SLUG"
fi

OUTPUT_PATH="$REPO_ROOT/notebooklm-auto/output/${BASENAME}.mp3"

echo "[*] Triggering NotebookLM Audio Overview for: $TARGET_INPUT"
./run.sh "$TARGET_INPUT" "$OUTPUT_PATH"
