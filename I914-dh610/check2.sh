#!/bin/bash
# #914, second run: hp/jet_by_order_check.py as fixed in the branch's commit f1d8f435a8 (its planted change survives
# rounding; the first run's rounded away), copied here, on #911's build (worktree choptuik-large-d-911 at 0cf9b94a,
# whose Python modules it imports), N 24, Np 6, 6 threads, nice 10. Exits 0 only when the series agree bit for bit
# and both controls differ.
set -u
WT=/home/nathan/Source/choptuik-large-d-911
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I914-dh610
ST=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $(git rev-parse --short HEAD), script md5 $(md5sum "$OUT/jet_by_order_check.py" | cut -c1-32), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/check2.log"
PYTHONPATH="$WT/hp" nice -n 10 python -u "$OUT/jet_by_order_check.py" "$RAW" "$ST" --N 24 --Np 6 --threads 6 --out "$OUT/by_order2" >> "$OUT/check2.log" 2>&1
RC=$?
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT/check2.log"
echo "exit $RC" >> "$OUT/check2.log"
exit $RC
