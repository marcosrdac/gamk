#!/usr/bin/env bash
# Minimal, Python-free first install for a genuinely new project directory.
# This intentionally does not migrate or overwrite existing agent context.
set -euo pipefail

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s TARGET_PROJECT_ROOT\n' "$0" >&2
    exit 64
fi

SOURCE_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$(mkdir -p -- "$1" && cd -- "$1" && pwd)"

# Keep this check deliberately conservative. Richer discovery/migration belongs to plan/install.py.
for signal in \
    "$TARGET_ROOT/AGENTS.md" \
    "$TARGET_ROOT/CLAUDE.md" \
    "$TARGET_ROOT/GEMINI.md" \
    "$TARGET_ROOT/.cursorrules" \
    "$TARGET_ROOT/.windsurfrules" \
    "$TARGET_ROOT/.clinerules" \
    "$TARGET_ROOT/.cursor/rules" \
    "$TARGET_ROOT/.github/instructions" \
    "$TARGET_ROOT/.cline/rules" \
    "$TARGET_ROOT/.roo/rules" \
    "$TARGET_ROOT/.windsurf/rules" \
    "$TARGET_ROOT/.ai"; do
    if [[ -e "$signal" || -L "$signal" ]]; then
        printf 'Copy install refused: existing project context at %s\n' "$signal" >&2
        printf 'No files were copied. Use scripts/install.sh plan %q for a migration-aware plan.\n' "$TARGET_ROOT" >&2
        exit 2
    fi
done

mkdir -p "$TARGET_ROOT/.ai"
for directory in \
    decisions forms/creating forms/pending forms/answered \
    analyses/doing analyses/closed/done analyses/closed/wontdo \
    logs rules skills templates wiki work/doing work/next \
    work/pool/backlog work/pool/blocked work/pool/ideas \
    work/closed/done work/closed/wontdo workflows; do
    mkdir -p "$TARGET_ROOT/.ai/$directory"
done

cp "$SOURCE_ROOT/.ai/templates/project/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
printf 'Files copied into %s\n' "$TARGET_ROOT"
printf '%s\n' \
    'This minimal installer did not configure a global link or write a provenance manifest.' \
    'For global linking, provenance, broader conflict detection, or migration planning, use scripts/install.sh.'
