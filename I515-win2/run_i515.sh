#!/usr/bin/env bash
# #515: near_null_eq.py --plant=7 at seven states of the first chain, four at a time (2 threads each, below normal priority), then the rows_only control at D 231.13 (must exit nonzero).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I515-win2
cd /d/choptuik-i505/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "0cce81e" ] || { echo "worktree D:/choptuik-i505 is not at 0cce81e" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
wave() {
  pids=()
  for spec in "$@"; do
    set -- $spec
    S=I461-win2/$1/anm_pin3_$2.npz
    [ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
    (
      echo "eq_$1_$2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
      nice -n 10 "$PY" -u near_null_eq.py $RAW $S --threads=2 --plant=7 --json=$R/eq_$1_$2.json > $R/eq_$1_$2.log 2>&1
      echo "eq_$1_$2 exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
    ) &
    pids+=($!)
  done
  wait "${pids[@]}"
}
wave "crawlB4 D228.1312" "crawlB4 D229.1312" "crawlB4 D230.1312" "crawlB4 D231.1312"
# wave 2: three states and the rows_only control at crawlB4 D 231.13, four processes
S=I461-win2/crawlB4/anm_pin3_D231.1312.npz
(
  echo "control eq_D231.1312 --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW $S --threads=2 --plant=7 --mutate=rows_only > $R/eq_B4_D231.1312_ctl_rows_only.log 2>&1
  echo "control eq_D231.1312 --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
) &
cpid=$!
wave "crawlB5 D234.1312" "crawlB5 D235.1312" "crawlE D239.8063"
wait $cpid
