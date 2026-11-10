#!/bin/bash
# lam_phys at D 55.04, M 64, kf 23 then kf 13.  Usage: run.sh WORKTREE PYTHON
wt=$1
py=$2
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
for K in 23 13
do
    start=$(date -u '+%Y-%m-%d %H:%M:%S')
    caffeinate -is nice -n 10 "$py" -u hp/gamma_dd.py "$out/gamma_M64_kf$K.jsonl" hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=$K > "$out/gamma_M64_kf$K.log" 2>&1
    echo "M64 kf$K exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
