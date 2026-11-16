#!/bin/bash
# #921: hp/jac_tangents_check.py on #608's state at D 253.338 (restart4_d6) with its chain's system and stored plan,
# tangents 1, 2, 4, 8, 6 threads, nice 10. The script exits 0 only when every n's Jacobian and the fastest n's Newton
# step are n = 1's bit for bit and the control differs.
set -u
WT=/home/nathan/Source/choptuik-large-d-921
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I921-dh610
ST=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/check.log"
nice -n 10 python -u jac_tangents_check.py "$RAW" "$ST" --threads 6 --ns 2,4,8 --out "$OUT/jac_tangents" >> "$OUT/check.log" 2>&1
RC=$?
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT/check.log"
echo "exit $RC" >> "$OUT/check.log"
exit $RC
