#!/bin/bash
# Issue #163: run one solver/rt script under nice into a log of this folder, with its exit code.
#   run_py.sh LOG script.py [args...]      (LOG relative to this folder)
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aed8a75ee3273b565
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
LOG="$HERE/$1"; shift
mkdir -p "$(dirname "$LOG")"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC $* (code $(git rev-parse --short HEAD))" > "$LOG"
nice -n 10 /Users/nathan/venv-qd/bin/python "solver/rt/$@" >> "$LOG" 2>&1
rc=$?
echo "== exit $rc" >> "$LOG"
exit $rc
