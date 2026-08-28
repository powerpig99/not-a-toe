#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT/notebooklm-auto"

SLUG="$1"

if [ -z "$SLUG" ]; then
    echo "Usage: ./scripts/generate-podcast.sh <slug-or-markdown-path>"
    echo "Example: ./scripts/generate-podcast.sh cong-xing-shi-mi-si-dao-luo-ji-bi-huan"
    exit 1
fi

# Resolve file path
if [ -f "$SLUG" ]; then
    SOURCE_PATH="$SLUG"
elif [ -f "$REPO_ROOT/content/posts/${SLUG}.md" ]; then
    SOURCE_PATH="$REPO_ROOT/content/posts/${SLUG}.md"
elif [ -f "$REPO_ROOT/export/${SLUG}.md" ]; then
    SOURCE_PATH="$REPO_ROOT/export/${SLUG}.md"
else
    echo "[-] File not found for: $SLUG"
    exit 1
fi

BASENAME="$(basename "$SOURCE_PATH" .md)"
OUTPUT_PATH="$REPO_ROOT/notebooklm-auto/output/${BASENAME}.mp3"

echo "[*] Generating podcast audio overview for: $BASENAME"
./run.sh "$SOURCE_PATH" "$OUTPUT_PATH"
