#!/bin/bash
# #571: the coordinator's commands (message of 2026-11-12 06:28 UTC): hp/modecount_ulp_circle.py with dh[10,11] moved by one unit in the
# last place of the double-double value (part lo), the R 0.01 circle around 3.1023 - 0.0068i on the kf 29 state, from the worktree's hp/.
# Usage: run_571.sh NAME SHIFT, with NAME shift0 (0) or lo_p1 (+1). The cap of the issue, 150 points on the circle: the cache holds those
# plus 2 beta points, so a run whose cache has more than 152 lines is stopped here and its exit is recorded as "cap".
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
name=$1
sh=$2
date -u +%FT%TZ > $raw/I571-macm3/$name/started.txt
caffeinate -is nice -n 10 python3 modecount_ulp_circle.py 10 11 $sh lo -- data/seeds/local/up23_D61.0264.npz 3.1023,-0.0068,0.01 --M=48 --kf=29 --n0=20 --fmax=1e-15 --data=$raw/I571-macm3/$name --res=$raw/I571-macm3/$name/circles.jsonl > $raw/I571-macm3/$name/circle.log 2>&1 &
job=$!
capped=no
while kill -0 $job 2>/dev/null; do
    sleep 20
    n=$(cat $raw/I571-macm3/$name/*evals.jsonl 2>/dev/null | wc -l)
    if [ "$n" -gt 152 ]; then
        capped=yes
        pkill -f "I571-macm3/$name"
        break
    fi
done
wait $job
code=$?
echo "$name exit $code at $(date -u +%FT%TZ) cap=$capped points=$(cat $raw/I571-macm3/$name/*evals.jsonl 2>/dev/null | wc -l)" >> $raw/I571-macm3/exits.txt
