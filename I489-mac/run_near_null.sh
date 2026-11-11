#!/usr/bin/env bash
# #489: hp/near_null.py on a polished state, then its control --mutate=sigma, 2 threads under nice 10.
# Usage: run_near_null.sh WORKTREE_HP RAW STATE TAG (STATE relative to RAW).
HP=$1
RAW=$2
S=$3
TAG=$4
R=$RAW/I489-mac
PY=/Users/nathan/venv-314/bin/python
cd "$HP" || exit 9
for MUT in none sigma; do
  t=$(date +%s)
  echo "near_null $TAG mutate=$MUT start $(date -u '+%Y-%m-%d %H:%M:%S UTC') on $S at $(git rev-parse --short=7 HEAD)" >> "$R/exits.txt"
  if [ "$MUT" = none ]; then
    nice -n 10 "$PY" -u near_null.py "$RAW" "$S" --threads=2 --json="$R/near_null_$TAG.json" > "$R/near_null_$TAG.log" 2>&1
  else
    nice -n 10 "$PY" -u near_null.py "$RAW" "$S" --threads=2 --mutate=sigma > "$R/near_null_${TAG}_ctl_sigma.log" 2>&1
  fi
  rc=$?
  echo "near_null $TAG mutate=$MUT exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
done
