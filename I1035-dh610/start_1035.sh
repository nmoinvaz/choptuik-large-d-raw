#!/bin/bash
# #1035 stage 2 planted run (dh610): starts unit i1035a (run1035.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1035-dh610 || exit 1
[ "$(systemctl --user is-active i1035a)" = active ] && { echo "i1035a active: not started"; exit 1; }
[ -e stage2_planted/exits_1035.txt ] && { echo "stage2_planted/exits_1035.txt exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1035a --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1035a bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1035a.log $PWD/run1035.sh 2>&1 | tail -1
