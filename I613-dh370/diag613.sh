#!/bin/bash
# Diagnosis of the one failed planted check of #613 (0.80, F = 1e-12): the same run again, and the neighbouring floors
# 5e-13 and 2e-12. Three at a time, 4 kernel threads each, nice 10.
# Run as: systemd-run --user --scope -p MemoryMax=26G -p MemorySwapMax=8G ./diag613.sh
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I613-dh370
cd "$WT/hp" && . ../.venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
st=I543-win2/renode_last080_D242.3642.npz
one() {  # name F
  local n=$1 F=$2
  { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') python near_null_eq.py $RAW $st --plant=7 --cr_floor=$F --threads=4 --json=$OUT/$n.json"
    /usr/bin/time -f "wall %e s, maxrss %M KB" nice -n 10 python near_null_eq.py "$RAW" "$st" --plant=7 --cr_floor=$F --threads=4 --json="$OUT/$n.json" 2>&1
    echo "exit $?"; } > "$OUT/$n.log" 2>&1
}
export -f one; export WT RAW OUT st
printf '%s\n' "diag_080_F1e-12_rerun 1e-12" "diag_080_F5e-13 5e-13" "diag_080_F2e-12 2e-12" | xargs -P3 -L1 bash -c 'one $0 $1'
echo "done $(date -u '+%H:%M')" > "$OUT/diag_done.txt"
