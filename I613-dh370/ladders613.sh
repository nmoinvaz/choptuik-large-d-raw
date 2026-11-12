#!/bin/bash
# #613's 16 runs: three at a time, each with 4 kernel threads, nice 10. Order: F = 1e-12 at the four layouts, then 1e-14,
# 1e-10, then the F = 0 controls.
# Run as: systemd-run --user --scope -p MemoryMax=26G -p MemorySwapMax=8G ./ladders613.sh
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I613-dh370
cd "$WT/hp" && . ../.venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
one() {  # layout F
  local lay=$1 F=$2
  case $lay in
    070)  st=I461-win2/crawlJ/anm_pin3_D242.3642.npz ;;
    080)  st=I543-win2/renode_last080_D242.3642.npz ;;
    092)  st=I554-win2/renode_last092_D242.3642.npz ;;
    0975) st=I562-win2/renode_0975_D242.3642.npz ;;
  esac
  local n=eq_${lay}_F$F
  { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') python near_null_eq.py $RAW $st --plant=7 --cr_floor=$F --threads=4 --json=$OUT/$n.json"
    /usr/bin/time -f "wall %e s, maxrss %M KB" nice -n 10 python near_null_eq.py "$RAW" "$st" --plant=7 --cr_floor=$F --threads=4 --json="$OUT/$n.json" 2>&1
    echo "exit $?"; } > "$OUT/$n.log" 2>&1
}
export -f one; export WT RAW OUT
printf '%s\n' "070 1e-12" "080 1e-12" "092 1e-12" "0975 1e-12" "070 1e-14" "080 1e-14" "092 1e-14" "0975 1e-14" \
  "070 1e-10" "080 1e-10" "092 1e-10" "0975 1e-10" "070 0" "080 0" "092 0" "0975 0" | xargs -P3 -L1 bash -c 'one $0 $1'
echo "all done $(date -u '+%H:%M')" > "$OUT/ladders_done.txt"
