#!/usr/bin/env bash
# #502: hp/near_null_eq.py on one state with one option set, 2 threads under nice 10, its exit and wall time appended
# to exits.txt. Usage: run_eq.sh WORKTREE_HP RAW STATE TAG [OPTIONS...] (STATE relative to RAW).
HP=$1
RAW=$2
S=$3
TAG=$4
shift 4
R=$RAW/I502-mac
PY=/Users/nathan/venv-314/bin/python
cd "$HP" || exit 9
t=$(date +%s)
echo "near_null_eq $TAG start $(date -u '+%Y-%m-%d %H:%M:%S UTC') on $S at $(git rev-parse --short=7 HEAD), options $*" >> "$R/exits.txt"
nice -n 10 "$PY" -u near_null_eq.py "$RAW" "$S" --threads=2 --json="$R/$TAG.json" "$@" > "$R/$TAG.log" 2>&1
rc=$?
echo "near_null_eq $TAG exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
exit $rc
