#!/usr/bin/env bash
# #554: x_last = 0.82 ... 0.92 (renode, near_null, near_null_eq; the renode control once at 0.86)
. /d/choptuik-large-d-raw/I554-win2/layout_lib.sh
for x in 082 084 086 088 090 092; do
  layout I554-win2 K last$x 0.3,0.4,0.5,0.6,0.${x:1}
  [ $x = 086 ] && ctl_renode I554-win2 K last086 0.3,0.4,0.5,0.6,0.86
done
echo "lane #554 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I554-win2/exits.txt
