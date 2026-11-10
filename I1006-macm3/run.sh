#!/bin/bash
# lam(48) at D 61.03, kf 27 then kf 25, --fmax=1e-18.  Usage: run.sh WORKTREE PYTHON
wt=$1
py=$2
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
for K in 27 25
do
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 "$py" -u hp/gamma_dd.py "$out/gamma_kf$K.jsonl" hp/data/seeds/local/up23_D61.0264.npz --threads=1 --polish=4 --M48 --kf48=$K --fmax=1e-18 > "$out/gamma_kf$K.log" 2>&1
    echo "kf$K exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
