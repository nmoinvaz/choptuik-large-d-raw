#!/bin/bash
# #1035 stage 2 planted run (dh610): starts unit i1035b (run1035_order.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1035-dh610 || exit 1
[ "$(systemctl --user is-active i1035b)" = active ] && { echo "i1035b active: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1035b --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1035b bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1035b.log $PWD/run1035_order.sh 2>&1 | tail -1
