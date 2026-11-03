#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -eq 0 ]]; then
    set -- plan
elif [[ "$1" == "init-mother" || "$1" == "plan-mother" ]]; then
    :
elif [[ "$1" != "plan" && "$1" != "install" && "$1" != "repair-link" && "$1" != "-h" && "$1" != "--help" ]]; then
    set -- plan "$@"
fi

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT_DIR/install.py" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$SCRIPT_DIR/install.py" "$@"
elif command -v nix >/dev/null 2>&1; then
    printf '%s\n' 'Python is not on PATH; launching through Nix (nixpkgs#python3).' >&2
    exec nix shell nixpkgs#python3 --command python3 "$SCRIPT_DIR/install.py" "$@"
else
    printf '%s\n' 'Python 3.10+ is required. Install Python or make python3 available through Nix.' >&2
    exit 127
fi
