#!/usr/bin/env bash
# #559: x_last = 0.94, 0.96, 0.98 (renode, near_null, near_null_eq; the renode control once at 0.96)
. /d/choptuik-large-d-raw/I559-win2/layout_lib.sh
for x in 094 096 098; do
  layout I559-win2 P last$x 0.3,0.4,0.5,0.6,0.${x:1}
  [ $x = 096 ] && ctl_renode I559-win2 P last096 0.3,0.4,0.5,0.6,0.96
done
echo "lane #559 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I559-win2/exits.txt
