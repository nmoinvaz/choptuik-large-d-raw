#!/usr/bin/env bash
# #505: near_null_eq.py --plant=7 at four states of crawlI/crawlJ, 2 threads each in parallel (below normal priority), then the rows_only control at D 237.13 (must exit nonzero).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I505-win2
cd /d/choptuik-i505/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "0cce81e" ] || { echo "worktree D:/choptuik-i505 is not at 0cce81e" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
pids=()
for spec in "crawlI D237.1312" "crawlJ D239.5375" "crawlJ D241.1244" "crawlJ D242.3642"; do
  set -- $spec
  S=I461-win2/$1/anm_pin3_$2.npz
  [ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
  (
    echo "eq_$2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
    nice -n 10 "$PY" -u near_null_eq.py $RAW $S --threads=2 --plant=7 --json=$R/eq_${2#D}.json > $R/eq_${2#D}.log 2>&1
    echo "eq_$2 exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  ) &
  pids+=($!)
done
wait "${pids[@]}"
echo "control eq_D237.1312 --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
nice -n 10 "$PY" -u near_null_eq.py $RAW I461-win2/crawlI/anm_pin3_D237.1312.npz --threads=2 --plant=7 --mutate=rows_only > $R/eq_D237.1312_ctl_rows_only.log 2>&1
echo "control eq_D237.1312 --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
