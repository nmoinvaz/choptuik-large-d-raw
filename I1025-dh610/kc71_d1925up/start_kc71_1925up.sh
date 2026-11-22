#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc71_d1925up || exit 1
[ "$(systemctl --user is-active i1025m)" = active ] && { echo "i1025m active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025m --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025m bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025m.log $PWD/lane_kc71_1925up.sh 2>&1 | tail -1
