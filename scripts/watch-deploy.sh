#!/usr/bin/env bash
# Deterministic GitHub Actions deployment watcher for not-a-toe.
# Polls until the workflow run for the target commit (default: HEAD) is registered,
# then polls run status to completion with interactive prompts disabled and
# bounded retries on transient GitHub API errors.

set -euo pipefail

export GH_PROMPT_DISABLED=1

TARGET_REF="${1:-HEAD}"
if ! COMMIT="$(git rev-parse --verify --end-of-options "${TARGET_REF}^{commit}" 2>/dev/null)"; then
  echo "Error: Unable to resolve commit '$TARGET_REF'." >&2
  exit 1
fi
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

POLL_INTERVAL="${WATCH_DEPLOY_POLL_SECS:-5}"
MAX_API_ERRORS=6
CONSECUTIVE_API_ERRORS=0
ERR_FILE="$(mktemp)"
trap 'rm -f "$ERR_FILE"' EXIT

while true; do
  STATUS=""
  CONCLUSION=""
  RUN_URL=""

  if RUN_INFO="$(gh run view "$RUN_ID" --json status,conclusion,url --jq '[.status, (.conclusion // "none"), (.url // "")] | join("|")' </dev/null 2>"$ERR_FILE")"; then
    IFS='|' read -r STATUS CONCLUSION RUN_URL <<< "$RUN_INFO"
  fi

  if [[ -z "$STATUS" ]]; then
    CONSECUTIVE_API_ERRORS=$((CONSECUTIVE_API_ERRORS + 1))
    ERR_MSG="$(tr '\r\n\t' '   ' < "$ERR_FILE" | tr -s ' ' | sed 's/^ //; s/ $//')"
    if (( CONSECUTIVE_API_ERRORS >= MAX_API_ERRORS )); then
      echo "Error: Failed to query GitHub Actions run $RUN_ID after $CONSECUTIVE_API_ERRORS consecutive API errors${ERR_MSG:+: $ERR_MSG}" >&2
      exit 1
    fi
    BACKOFF_SECS=$((POLL_INTERVAL * CONSECUTIVE_API_ERRORS))
    echo "Warning: Transient error querying run $RUN_ID ($CONSECUTIVE_API_ERRORS/$MAX_API_ERRORS)${ERR_MSG:+: $ERR_MSG}; retrying in ${BACKOFF_SECS}s..." >&2
    sleep "$BACKOFF_SECS"
    continue
  fi

  CONSECUTIVE_API_ERRORS=0

  if [[ "$STATUS" == "completed" ]]; then
    if [[ "$CONCLUSION" == "success" ]]; then
      echo "GitHub Actions run $RUN_ID completed with 'success'${RUN_URL:+ ($RUN_URL)}."
      exit 0
    fi
    echo "Error: GitHub Actions run $RUN_ID completed with '$CONCLUSION'${RUN_URL:+ ($RUN_URL)}." >&2
    gh run view "$RUN_ID" </dev/null >&2 || true
    exit 1
  fi

  sleep "$POLL_INTERVAL"
done
