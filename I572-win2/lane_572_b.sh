#!/usr/bin/env bash
# #572 lane B: x_last = 0.98 (with the renode control) and 0.99 at crawlI D 237.1312
. /d/choptuik-large-d-raw/I572-win2/layout_lib.sh
J=I461-win2/crawlI/anm_pin3_D237.1312.npz
layout I572-win2 B last098 0.3,0.4,0.5,0.6,0.98
ctl_renode I572-win2 B last098 0.3,0.4,0.5,0.6,0.98
layout I572-win2 B last099 0.3,0.4,0.5,0.6,0.99
echo "lane B done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I572-win2/exits.txt
