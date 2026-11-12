#!/usr/bin/env bash
# #572 lane A: x_last = 0.95 and 0.97 at crawlI D 237.1312
. /d/choptuik-large-d-raw/I572-win2/layout_lib.sh
J=I461-win2/crawlI/anm_pin3_D237.1312.npz
for x in 095 097; do layout I572-win2 A last$x 0.3,0.4,0.5,0.6,0.${x:1}; done
echo "lane A done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I572-win2/exits.txt
