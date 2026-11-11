#!/bin/bash
# Usage: run.sh WORKTREE PYTHON
wt=$1
py=$2
raw=$(cd "$(dirname "$0")/.." && pwd)
cd "$wt" || exit 2
start=$(date -u '+%Y-%m-%d %H:%M:%S')
caffeinate -is nice -n 10 "$py" -u hp/gamma_m48_gap.py analyze "$raw/I451-macm3/analyze_D58.jsonl" "$raw/I266-mac/states/up12_D58.0060_M48_r2.npz" "$raw/I266-mac/states/up12_D58.0060_M48_r2_qd.npz" --w=24 --threads=1 --lam > "$raw/I451-macm3/analyze_D58.log" 2>&1
echo "analyze exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$raw/I451-macm3/exits.txt"
