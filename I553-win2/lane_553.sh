#!/usr/bin/env bash
# #553: the new layouts 0.73, 0.75, 0.77, 0.78, 0.79 (renode, near_null_vec, near_null_eq; the renode control once at 0.77), then near_null_vec on the existing layouts 0.72, 0.74, 0.76, 0.80
. /d/choptuik-large-d-raw/I553-win2/layout_lib.sh
. /d/choptuik-large-d-raw/I553-win2/layout_lib_vec.sh
for x in 073 075 077 078 079; do
  layout_vec I553-win2 L last$x 0.3,0.4,0.5,0.6,0.${x:1}
  [ $x = 077 ] && ctl_renode I553-win2 L last077 0.3,0.4,0.5,0.6,0.77
done
nn_vec I553-win2 L old072 I537-win2/renode_last072_D242.3642.npz
nn_vec I553-win2 L old074 I543-win2/renode_last074_D242.3642.npz
nn_vec I553-win2 L old076 I543-win2/renode_last076_D242.3642.npz
nn_vec I553-win2 L old080 I543-win2/renode_last080_D242.3642.npz
echo "lane #553 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I553-win2/exits.txt
