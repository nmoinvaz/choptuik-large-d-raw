#!/usr/bin/env bash
# #566 lane B: new layout 0.99 (with the renode control), then the vectors of the existing 0.98
. /d/choptuik-large-d-raw/I566-win2/layout_lib.sh
. /d/choptuik-large-d-raw/I566-win2/lib_566.sh
newlayout B last099 0.3,0.4,0.5,0.6,0.99
ctl_renode $F B last099 0.3,0.4,0.5,0.6,0.99
vecs B old098 I559-win2/renode_last098_D242.3642.npz 0
echo "lane B done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
