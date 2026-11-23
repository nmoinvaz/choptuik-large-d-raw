#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/cross_macm3_d1975 || exit 1
[ "$(systemctl --user is-active i1025x)" = active ] && { echo "i1025x active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025x --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025x bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025x.log $PWD/lane_cross.sh 2>&1 | tail -1
