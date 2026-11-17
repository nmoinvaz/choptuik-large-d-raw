#!/bin/bash
# #944: stop a control run (junk 0) after the a = 1 attempt has ended, i.e. once its "a 1.000 -> D ..." result line is in the log.
# usage: stop_after_a1.sh NAME. Prints that line, kills the run and records it in exits_944.txt.
NAME=${1:?name}
OUT=$HOME/Source/choptuik-large-d-raw/I944-dh170
while ! grep -q '^    a 1\.000 -> D ' $OUT/$NAME.log 2>/dev/null; do
  pgrep -f "^timeout .*anm_run.py .*$OUT/$NAME " > /dev/null || { echo "run $NAME ended before its a = 1 line"; exit 1; }
  sleep 5
done
grep -n -B3 '^    a 1\.000 -> D ' $OUT/$NAME.log | cut -c1-300
pkill -TERM -f "^timeout .*anm_run.py .*$OUT/$NAME "
echo "944 $NAME stopped by me after the a = 1 attempt (control) $(date -u '+%F %T') UTC" >> $OUT/exits_944.txt
