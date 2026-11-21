#!/bin/bash
# #1067 (dh610): starts unit i1067a (run1067.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 1
[ "$(systemctl --user is-active i1067a)" = active ] && { echo "i1067a active: not started"; exit 1; }
[ -e stage1.log ] && { echo "stage1.log exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1067a --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1067a bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1067a.log $PWD/run1067.sh 2>&1 | tail -1
