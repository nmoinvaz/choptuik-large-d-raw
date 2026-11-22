#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc71_d19125 || exit 1
[ "$(systemctl --user is-active i1025h)" = active ] && { echo "i1025h active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025h --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025h bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025h.log $PWD/lane_kc71.sh 2>&1 | tail -1
