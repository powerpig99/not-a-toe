#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

node build.mjs

if [[ $# -gt 0 ]]; then
  "$@"
fi
