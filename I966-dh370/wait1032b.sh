#!/usr/bin/env bash
# #1032 after accuracy exited 1 (reported): wakes when acc_sign and acc_nobar both have an exit line, at once if one exits 0, has a Traceback, or the unit ends.
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370
while sleep 15; do
  n=0
  for c in acc_sign acc_nobar; do
    [ -f $D/$c.log ] || continue
    e=$(grep -m1 '^exit ' $D/$c.log | cut -d' ' -f2); [ -z "$e" ] && continue
    n=$((n+1))
    [ "$e" != 1 ] && { echo "CONTROL $c exit $e (want 1)"; tail -3 $D/$c.log | cut -c1-200; exit 0; }
    grep -q '^Traceback' $D/$c.log && { echo "CONTROL $c exited 1 with a Traceback"; exit 0; }
  done
  [ $n -ge 2 ] && { echo "CONTROLS DONE 2"; exit 0; }
  [ "$(systemctl --user is-active i1032a)" != active ] && { echo "UNIT ENDED early, $n controls done"; exit 0; }
done
