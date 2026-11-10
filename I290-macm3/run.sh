#!/bin/bash
# lam_phys at D 61.03, M 48 at five cuts, one after another.  Usage: run.sh WORKTREE PYTHON
wt=$1
py=$2
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
for K in 13 21 23 25 27
do
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 "$py" -u hp/gamma_dd.py "$out/gamma_kf$K.jsonl" hp/data/seeds/local/up23_D61.0264.npz --threads=1 --polish=4 --M48 --kf48=$K > "$out/gamma_kf$K.log" 2>&1
    echo "kf$K exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
