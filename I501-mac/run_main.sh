#!/usr/bin/env bash
# #501: origin/main's hp/near_null.py (53d8b78, last changed in 3bd9d1b), copied into the worktree's hp as
# near_null_main.py, on the 0.3-0.8 start: its lines are the reference for the existing lines of near_null_s08.log.
# Usage: run_main.sh WORKTREE_HP RAW, 2 threads, nice 10.
HP=$1
RAW=$2
R=$RAW/I501-mac
PY=/Users/nathan/venv-314/bin/python
S08=I489-mac/renode_L1_horizon_D242.3642.npz
cd "$HP" || exit 9
t=$(date +%s)
echo "s08_main start $(date -u '+%Y-%m-%d %H:%M:%S UTC'): origin/main 53d8b78's near_null.py as near_null_main.py, RAW $S08 --threads=2" >> "$R/exits.txt"
nice -n 10 "$PY" -u near_null_main.py "$RAW" "$S08" --threads=2 > "$R/near_null_s08_main.log" 2>&1
rc=$?
echo "s08_main exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
