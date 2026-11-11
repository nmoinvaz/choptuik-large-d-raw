#!/usr/bin/env bash
# #516 part 2b: near_null_eq.py --plant=7 on the attempt's state (D 239.8063, clean chain, main 14dc386) and on crawlE's D 239.8063, in parallel, 2 threads each (worktree D:/choptuik-i505 at 0cce81e).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I516-win2
cd /d/choptuik-i505/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "0cce81e" ] || { echo "worktree D:/choptuik-i505 is not at 0cce81e" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
(
  echo "eq_attempt_D239.8063 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW I516-win2/attempt/anm_pin3_D239.8063.npz --threads=2 --plant=7 --json=$R/eq_attempt_D239.8063.json > $R/eq_attempt_D239.8063.log 2>&1
  echo "eq_attempt_D239.8063 exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
) &
p1=$!
(
  echo "eq_crawlE_D239.8063 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW I461-win2/crawlE/anm_pin3_D239.8063.npz --threads=2 --plant=7 --json=$R/eq_crawlE_D239.8063.json > $R/eq_crawlE_D239.8063.log 2>&1
  echo "eq_crawlE_D239.8063 exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
) &
p2=$!
wait $p1 $p2
