#!/usr/bin/env bash
# #504: hp/eq_test.py SUBCOMMAND ARGS... with 2 threads under nice 10, its log I504-mac/TAG.log, its exit and wall time
# appended to I504-mac/exits.txt. Usage: run_eq.sh WORKTREE_HP OUTRAW TAG SUBCOMMAND ARGS...
HP=$1
R=$2/I504-mac
TAG=$3
shift 3
PY=/Users/nathan/venv-314/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
cd "$HP" || exit 9
t=$(date +%s)
echo "$TAG start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at $(git rev-parse --short=7 HEAD): eq_test.py $*" >> "$R/exits.txt"
nice -n 10 "$PY" -u eq_test.py "$@" > "$R/$TAG.log" 2>&1
rc=$?
echo "$TAG exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
exit $rc
