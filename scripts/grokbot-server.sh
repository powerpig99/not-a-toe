#!/bin/bash
# Grok Bot local MCP server (the bridge to Grok Bot's Dispatcher), started only on demand.
#   bash scripts/grokbot-server.sh start    # serve http://127.0.0.1:3000/v1/mcp in the background
#   bash scripts/grokbot-server.sh status   # is it answering?
#   bash scripts/grokbot-server.sh stop     # stop it when the exchange is done
# Project: ~/grokbot (agent-sdk). The bearer token lives in ~/grokbot/.env as TOKEN and is never printed.
# The token is the same one in ~/.gemini/config/mcp_config.json (grokbot). Protocol: docs/wave-refinement-plan.md §8.2.
set -euo pipefail
DIR="$HOME/grokbot"
PIDF="$DIR/.agent-serve/server.pid"
LOG="$DIR/.agent-serve/server.log"
URL="http://127.0.0.1:3000/"

answering() { [ "$(curl -s -m 3 -o /dev/null -w '%{http_code}' "$URL" || true)" != "000" ]; }

case "${1:-status}" in
  start)
    if answering; then echo "already running ($URL)"; exit 0; fi
    cd "$DIR"
    set -a; . ./.env; set +a
    nohup agent-sdk serve --dir "$DIR" --mode single --bearer-token "$TOKEN" </dev/null >"$LOG" 2>&1 &
    echo $! > "$PIDF"
    for _ in $(seq 1 20); do answering && { echo "started (pid $(cat "$PIDF"), $URL, log $LOG)"; exit 0; }; sleep 1; done
    echo "did not answer within 20 s; see $LOG" >&2; exit 1 ;;
  stop)
    if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then kill "$(cat "$PIDF")"; rm -f "$PIDF"; fi
    pkill -f "agent-sdk serve --dir $DIR" 2>/dev/null || true
    sleep 1
    if answering; then echo "still answering on $URL" >&2; exit 1; fi
    echo "stopped" ;;
  status)
    if answering; then echo "running ($URL)"; else echo "stopped"; fi ;;
  *) echo "usage: $0 start|stop|status" >&2; exit 2 ;;
esac
