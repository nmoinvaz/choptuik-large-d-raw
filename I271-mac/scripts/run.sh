#!/bin/bash
# Run one command from the worktree root at nice 10 under caffeinate, log it to I271-mac/logs/<name>.log and append
# its exit to logs/exits.txt.  Usage: run.sh NAME WORKTREE CMD...
name=$1
wt=$2
shift 2
here=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$here/logs"
cd "$wt" || exit 2
start=$(date -u '+%Y-%m-%d %H:%M')
caffeinate -i nice -n 10 "$@" > "$here/logs/$name.log" 2>&1
rc=$?
echo "$name exit $rc ($start to $(date -u '+%H:%M') UTC): $*" >> "$here/logs/exits.txt"
exit $rc
