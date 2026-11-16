#!/bin/bash
# #898: hp/jet_lanes_check.py on #608's stored series at D 253.338 (restart4_d6, step 5) with the solver of its state
# (stored plan), 6 threads, nice 10; then its control (--mutate 1), which must exit 1. Exit 0 when both behave.
set -u
WT=/home/nathan/Source/choptuik-large-d-898
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I898-dh610
SER=I608-dh610/restart4_d6/jet_pin3_D253.3382.npz
ST=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/check.log"
nice -n 10 python -u jet_lanes_check.py "$RAW" "$SER" "$ST" --threads 6 --out "$OUT/lanes" >> "$OUT/check.log" 2>&1
RC1=$?
echo "exit $RC1" >> "$OUT/check.log"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC control, load $(cut -d' ' -f1-3 /proc/loadavg)" > "$OUT/control.log"
nice -n 10 python -u jet_lanes_check.py "$RAW" "$SER" "$ST" --threads 6 --mutate 1 --out "$OUT/lanes_mutate1" >> "$OUT/control.log" 2>&1
RC2=$?
echo "exit $RC2 (must be 1)" >> "$OUT/control.log"
[ $RC1 -eq 0 ] && [ $RC2 -eq 1 ]
