#!/bin/bash
# Message Grok Bot's Dispatcher through a handoff file (the message carries only path + sha256).
#   bash scripts/grokbot-msg.sh send <path/to/HANDOFF.md>   # sends "HANDOFF <path> sha256 <hash>"
#   bash scripts/grokbot-msg.sh check                       # read what the Dispatcher sent since the last read
#   bash scripts/grokbot-msg.sh verify <path/to/RESULT.md> <sha256>   # recompute a returned file's hash
# Needs the server: bash scripts/grokbot-server.sh start. Every raw response is appended to
# ~/grokbot/.agent-serve/messages.log, because check advances a read cursor: a reply read once is not returned again.
set -euo pipefail
DIR="$HOME/grokbot"; LOG="$DIR/.agent-serve/messages.log"; AGENT="${GROKBOT_AGENT:-Dispatcher}"

call() {  # $1 = JSON params for tools/call
  set -a; . "$DIR/.env"; set +a
  local out
  out=$(curl -s -m 120 -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' -X POST http://127.0.0.1:3000/v1/mcp \
        -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":$1}")
  printf '%s\t%s\n' "$(date -u +%FT%TZ)" "$out" >> "$LOG"
  printf '%s' "$out" | python3 -c '
import json,sys
r=json.load(sys.stdin); t=json.loads(r["result"]["content"][0]["text"]); x=t.get("result",{}) or {}
print("STATUS:", x.get("status") or ("ERROR: "+str(t.get("errorMessage"))))
for k in ("earlierReplies","reply"):
    v=x.get(k)
    if v: print("==",k,"=="); print(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=1))'
}

case "${1:-}" in
  send)
    f="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; h=$(shasum -a 256 "$f" | awk '{print $1}')
    msg="HANDOFF $f sha256 $h — from the Antigravity Dispatcher. Recompute the sha256 before acting; write your answer to RESULT.md beside it and reply with its path and sha256."
    call "$(python3 -c 'import json,sys;print(json.dumps({"name":"call_tool","arguments":{"toolName":"grokbot__ask","input":{"agent":sys.argv[1],"message":sys.argv[2],"waitSeconds":30}}}))' "$AGENT" "$msg")" ;;
  check)
    call "$(python3 -c 'import json,sys;print(json.dumps({"name":"call_tool","arguments":{"toolName":"grokbot__check","input":{"agent":sys.argv[1],"waitSeconds":30}}}))' "$AGENT")" ;;
  verify)
    got=$(shasum -a 256 "$2" | awk '{print $1}'); [ "$got" = "$3" ] && echo "OK $2" || { echo "MISMATCH $2: $got != $3" >&2; exit 1; } ;;
  *) echo "usage: $0 send <HANDOFF.md> | check | verify <RESULT.md> <sha256>" >&2; exit 2 ;;
esac
