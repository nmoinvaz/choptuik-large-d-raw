#!/bin/bash
# #613's ladder on main ff08351: 14 runs, three at a time, 4 kernel threads each, nice 10, no memory guard.
# Order: F = 1e-12 at the four layouts, then 5e-13 and 2e-12 at 0.80, then 1e-14 and 1e-10 at all four.
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I613-dh370/rerun_ff08351
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
  { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') python near_null_eq.py $RAW $st --plant=7 --cr_sets --cr_floor=$F --threads=4 --json=$OUT/$n.json"
    /usr/bin/time -f "wall %e s, maxrss %M KB" nice -n 10 python near_null_eq.py "$RAW" "$st" --plant=7 --cr_sets --cr_floor=$F --threads=4 --json="$OUT/$n.json" 2>&1
    echo "exit $?"; } > "$OUT/$n.log" 2>&1
}
export -f one; export WT RAW OUT
printf '%s\n' "070 1e-12" "080 1e-12" "092 1e-12" "0975 1e-12" "080 5e-13" "080 2e-12" \
  "070 1e-14" "080 1e-14" "092 1e-14" "0975 1e-14" "070 1e-10" "080 1e-10" "092 1e-10" "0975 1e-10" | xargs -P3 -L1 bash -c 'one $0 $1'
echo "all done $(date -u '+%H:%M')" > "$OUT/rerun_done.txt"
