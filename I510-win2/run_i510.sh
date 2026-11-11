#!/usr/bin/env bash
# #510: near_null_eq.py --plant=7 at eight states, four at a time (2 threads each, below normal priority), then the rows_only control at D 216.13 (must exit nonzero).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I510-win2
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
      nice -n 10 "$PY" -u near_null_eq.py $RAW $S --threads=2 --plant=7 --json=$R/eq_$2.json > $R/eq_$2.log 2>&1
      echo "eq_$1_$2 exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
    ) &
    pids+=($!)
  done
  wait "${pids[@]}"
}
wave "crawlG D216.1312" "crawlG D220.1312" "crawlG D224.1312" "crawlG D228.1312"
wave "crawlG D232.1312" "crawlI D235.1312" "crawlL D242.5225" "probeH00390625 D242.5264"
echo "control eq_D216.1312 --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
nice -n 10 "$PY" -u near_null_eq.py $RAW I461-win2/crawlG/anm_pin3_D216.1312.npz --threads=2 --plant=7 --mutate=rows_only > $R/eq_D216.1312_ctl_rows_only.log 2>&1
echo "control eq_D216.1312 --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
