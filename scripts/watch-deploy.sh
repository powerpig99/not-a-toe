#!/usr/bin/env bash
# Deterministic GitHub Actions deployment watcher for not-a-toe.
# Polls until the workflow run for the target commit (default: HEAD) is registered,
# then watches it to completion with interactive prompts strictly disabled.

set -euo pipefail

export GH_PROMPT_DISABLED=1

COMMIT="${1:-$(git rev-parse HEAD)}"
SITE_PATHS_RE='^(content/|data/|assets/|build\.mjs$|style\.css$|package.*\.json$|\.github/workflows/deploy\.yml$)'

if ! git diff-tree --no-commit-id --name-only -r "$COMMIT" | grep -qE "$SITE_PATHS_RE"; then
  EXISTING_RUN="$(gh run list --commit "$COMMIT" --limit 1 --json databaseId --jq '.[0].databaseId // empty' </dev/null || true)"
  if [[ -z "$EXISTING_RUN" ]]; then
    echo "No site-input changes in commit $COMMIT; GitHub Pages deploy not required (skipped)."
    exit 0
  fi
fi

MAX_ATTEMPTS=15
SLEEP_SECS=2
RUN_ID=""

for ((i = 1; i <= MAX_ATTEMPTS; i++)); do
  RUN_ID="$(gh run list --commit "$COMMIT" --limit 1 --json databaseId --jq '.[0].databaseId // empty' </dev/null || true)"
  if [[ -n "$RUN_ID" ]]; then
    break
  fi
  sleep "$SLEEP_SECS"
done

if [[ -z "$RUN_ID" ]]; then
  echo "Error: No GitHub Actions workflow run registered for commit $COMMIT after $((MAX_ATTEMPTS * SLEEP_SECS))s." >&2
  exit 1
fi

echo "Watching GitHub Actions run $RUN_ID for commit $COMMIT..."
exec gh run watch "$RUN_ID" --exit-status </dev/null
