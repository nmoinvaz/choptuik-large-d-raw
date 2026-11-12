#!/bin/bash
# #613's rerun of the 0.80 bracket on main 54c9fcb, with --cr_sets: F = 5e-13, 1e-12, 2e-12 at once, 4 kernel threads
# each, nice 10.
# Run as: systemd-run --user --scope -p MemoryMax=26G -p MemorySwapMax=8G ./rerun.sh
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I613-dh370/rerun_54c9fcb
cd "$WT/hp" && . ../.venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
st=I543-win2/renode_last080_D242.3642.npz
one() {
  local F=$1 n=eq_080_F$1
  { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') python near_null_eq.py $RAW $st --plant=7 --cr_sets --cr_floor=$F --threads=4 --json=$OUT/$n.json"
    /usr/bin/time -f "wall %e s, maxrss %M KB" nice -n 10 python near_null_eq.py "$RAW" "$st" --plant=7 --cr_sets --cr_floor=$F --threads=4 --json="$OUT/$n.json" 2>&1
    echo "exit $?"; } > "$OUT/$n.log" 2>&1
}
export -f one; export WT RAW OUT st
printf '%s\n' 5e-13 1e-12 2e-12 | xargs -P3 -L1 bash -c 'one $0'
echo "done $(date -u '+%H:%M')" > "$OUT/rerun_done.txt"
