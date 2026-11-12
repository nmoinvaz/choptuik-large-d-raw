#!/usr/bin/env bash
# #566 lane A: new layouts 0.97 and 0.995, then the vectors of the existing 0.96
. /d/choptuik-large-d-raw/I566-win2/layout_lib.sh
. /d/choptuik-large-d-raw/I566-win2/lib_566.sh
newlayout A last097 0.3,0.4,0.5,0.6,0.97
newlayout A last0995 0.3,0.4,0.5,0.6,0.995
vecs A old096 I559-win2/renode_last096_D242.3642.npz 0
echo "lane A done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
