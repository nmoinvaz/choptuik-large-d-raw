#!/bin/bash
# lam(48) at kf 13 and kf 15 at D 40, 50 and 58.  Usage: run.sh WORKTREE PYTHON
wt=$1
py=$2
out=$(cd "$(dirname "$0")" && pwd)
cd "$wt" || exit 2
for S in up7_D40.0201 up8_D50.0075 up12_D58.0060
do
    for K in 13 15
    do
        start=$(date -u '+%Y-%m-%d %H:%M:%S')
        caffeinate -is nice -n 10 "$py" -u hp/gamma_dd.py "$out/gamma_${S}_kf$K.jsonl" hp/data/states/$S.npz --threads=1 --polish=4 --M48 --kf48=$K > "$out/gamma_${S}_kf$K.log" 2>&1
        echo "$S kf$K exit $? ($start to $(date -u '+%H:%M:%S') UTC)" >> "$out/exits.txt"
    done
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S')" >> "$out/exits.txt"
