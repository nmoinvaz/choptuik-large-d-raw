#!/bin/bash
# Control for #580: the same planted check at F = 0 (no floor) on this kernel at the four layouts, three at a time.
# Run as: systemd-run --user --scope -p MemoryMax=26G -p MemorySwapMax=8G ./f0_580.sh
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I580-dh370
cd "$WT/hp" && . ../.venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
one() {  # layout
  local lay=$1
  case $lay in
    070)  st=I461-win2/crawlJ/anm_pin3_D242.3642.npz ;;
    080)  st=I543-win2/renode_last080_D242.3642.npz ;;
    092)  st=I554-win2/renode_last092_D242.3642.npz ;;
    0975) st=I562-win2/renode_0975_D242.3642.npz ;;
  esac
  local n=eq_${lay}_F0
  { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') python near_null_eq.py $RAW $st --plant=7 --cr_floor=0 --threads=4 --json=$OUT/$n.json"
    /usr/bin/time -f "wall %e s, maxrss %M KB" nice -n 10 python near_null_eq.py "$RAW" "$st" --plant=7 --cr_floor=0 --threads=4 --json="$OUT/$n.json" 2>&1
    echo "exit $?"; } > "$OUT/$n.log" 2>&1
}
export -f one; export WT RAW OUT
printf '%s\n' 070 080 092 0975 | xargs -P3 -L1 bash -c 'one $0'
echo "done $(date -u '+%H:%M')" > "$OUT/f0_done.txt"
