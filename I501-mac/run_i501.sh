#!/usr/bin/env bash
# #501: hp/near_null.py's first Newton step, the planted check and its control, then the two states.
# Usage: run_i501.sh WORKTREE_HP RAW RUN...   (RUN: planted, control, s08, s08_keep, s07_keep), 2 threads, nice 10.
HP=$1
RAW=$2
shift 2
R=$RAW/I501-mac
PY=/Users/nathan/venv-314/bin/python
S07=I461-win2/crawlJ/anm_pin3_D242.3642.npz
S08=I489-mac/renode_L1_horizon_D242.3642.npz
cd "$HP" || exit 9
for RUN in "$@"; do
  case $RUN in
    planted) A=("$S07" --planted=1 --json="$R/near_null_planted.json") ;;
    control) A=("$S07" --planted=1 --mutate=scale_block --json="$R/near_null_planted_ctl_scale_block.json") ;;
    s08) A=("$S08" --json="$R/near_null_s08.json") ;;
    s08_keep) A=("$S08" --keep_plan=1 --json="$R/near_null_s08_keep.json") ;;
    s07_keep) A=("$S07" --keep_plan=1 --json="$R/near_null_s07_keep.json") ;;
    *) echo "unknown run $RUN"; exit 9 ;;
  esac
  t=$(date +%s)
  echo "$RUN start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at $(git rev-parse --short=7 HEAD): near_null.py RAW ${A[*]} --threads=2" >> "$R/exits.txt"
  nice -n 10 "$PY" -u near_null.py "$RAW" "${A[@]}" --threads=2 > "$R/near_null_$RUN.log" 2>&1
  rc=$?
  echo "$RUN exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
done
