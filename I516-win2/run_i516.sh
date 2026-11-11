#!/usr/bin/env bash
# #516 part 1: near_null_eq.py --plant=7 at nine half-unit states, four at a time (2 threads each, below normal priority), and the rows_only control at crawlG D 232.63 (must exit nonzero).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I516-win2
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
wave "crawlG D232.6312" "crawlI D233.6312" "crawlI D234.6312" "crawlI D235.6312"
wave "crawlI D236.6312" "crawlB4 D231.6312" "crawlB5 D232.6312" "crawlB5 D233.6312"
S=I461-win2/crawlG/anm_pin3_D232.6312.npz
(
  echo "control eq_crawlG_D232.6312 --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW $S --threads=2 --plant=7 --mutate=rows_only > $R/eq_crawlG_D232.6312_ctl_rows_only.log 2>&1
  echo "control eq_crawlG_D232.6312 --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
) &
cpid=$!
wave "crawlB5 D235.6312"
wait $cpid
