#!/bin/bash
# #1035 stage 3 (dh610): starts unit i1035c (run1035_stage3.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1035-dh610 || exit 1
[ "$(systemctl --user is-active i1035c)" = active ] && { echo "i1035c active: not started"; exit 1; }
[ -e stage2/exits_1035_stage3.txt ] && { echo "stage2/exits_1035_stage3.txt exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1035c --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1035c bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1035c.log $PWD/run1035_stage3.sh 2>&1 | tail -1
