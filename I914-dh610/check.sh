#!/bin/bash
# #914: hp/jet_by_order_check.py on #911's build (worktree choptuik-large-d-911 at 0cf9b94a), on #608's state at D 253.338 (restart4_d6) with its chain's system and stored plan,
# N 24, Np 6, 6 threads, nice 10. The script exits 0 only when the series agree bit for bit and both controls differ.
set -u
WT=/home/nathan/Source/choptuik-large-d-911
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I914-dh610
ST=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/check.log"
nice -n 10 python -u jet_by_order_check.py "$RAW" "$ST" --N 24 --Np 6 --threads 6 --out "$OUT/by_order" >> "$OUT/check.log" 2>&1
RC=$?
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT/check.log"
echo "exit $RC" >> "$OUT/check.log"
exit $RC
