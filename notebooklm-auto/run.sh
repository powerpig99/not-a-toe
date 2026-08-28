#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BRAVE_APP="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
CDP_PORT=9222
CDP_URL="http://localhost:${CDP_PORT}/json/version"

echo "========================================================"
echo "  NotebookLM Podcast Generator (macOS + Brave CDP)      "
echo "========================================================"

# 1. Check / Setup Python environment
if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment (.venv)..."
    if command -v uv >/dev/null 2>&1; then
        uv venv .venv
        source .venv/bin/activate
        uv pip install -r requirements.txt
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    fi
else
    source .venv/bin/activate
fi

# 2. Check if Brave CDP port is reachable
echo "[*] Checking Brave CDP connection on port ${CDP_PORT}..."
if curl -s "${CDP_URL}" >/dev/null 2>&1; then
    echo "[+] Brave is already running with remote debugging port ${CDP_PORT}."
else
    echo "[!] Brave is NOT listening on port ${CDP_PORT}."
    
    if [ -f "${BRAVE_APP}" ]; then
        echo "[*] Launching Brave Browser with --remote-debugging-port=${CDP_PORT}..."
        "${BRAVE_APP}" --remote-debugging-port=${CDP_PORT} >/dev/null 2>&1 &
        
        WAITED=0
        while ! curl -s "${CDP_URL}" >/dev/null 2>&1; do
            sleep 1
            WAITED=$((WAITED + 1))
            if [ ${WAITED} -ge 15 ]; then
                echo "[-] ERROR: Timed out waiting for Brave to start on port ${CDP_PORT}."
                echo "[-] If Brave is already open without debugging port enabled, please close Brave completely (Cmd+Q) and re-run this script."
                exit 1
            fi
        done
        echo "[+] Brave started and CDP port is ready."
    else
        echo "[-] ERROR: Brave Browser app not found at ${BRAVE_APP}."
        exit 1
    fi
fi

# 3. Handle arguments: URL or local file
INPUT_ARG=""
OUTPUT_ARG=""

if [ -n "$1" ]; then
    if [[ "$1" == http://* ]] || [[ "$1" == https://* ]]; then
        INPUT_ARG="--url $1"
        BASENAME="$(echo "$1" | sed 's:/*$::' | awk -F/ '{print $NF}')"
        OUTPUT_ARG="--output ./output/${BASENAME}.mp3"
    else
        INPUT_ARG="--source $1"
        BASENAME="$(basename "$1" .md)"
        OUTPUT_ARG="--output ./output/${BASENAME}.mp3"
    fi
    
    if [ -n "$2" ]; then
        OUTPUT_ARG="--output $2"
    fi
fi

# 4. Execute python automation script
echo "[*] Executing generate_podcast.py..."
python3 generate_podcast.py ${INPUT_ARG} ${OUTPUT_ARG} "${@:3}"

echo "========================================================"
echo "  Process completed!                                    "
echo "========================================================"
