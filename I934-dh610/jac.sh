#!/bin/bash
# #934: hp/jac_tangents_check.py on #608's state at D 253.338 (restart4_d6), n = 1 against n = 2 (the new default),
# 5 threads, nice 10. Exits 0 only when the n = 2 Jacobian and Newton step are n = 1's bit for bit and the control
# differs.
taskset -cp 0-4 $$ > /dev/null  # 5 of the 20 CPUs: two chains use the rest
set -u
WT=/home/nathan/Source/choptuik-large-d-934
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
ST=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/jac.log"
nice -n 10 python -u jac_tangents_check.py "$RAW" "$ST" --threads 5 --ns 2 --out "$OUT/jac_tangents" >> "$OUT/jac.log" 2>&1
RC=$?
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT/jac.log"
echo "exit $RC" >> "$OUT/jac.log"
exit $RC
