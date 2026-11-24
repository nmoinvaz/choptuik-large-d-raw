#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_d21 || exit 1
[ "$(systemctl --user is-active i1025an)" = active ] && { echo "i1025an active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025an --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025an bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025an.log $PWD/lane_kc87_d21.sh 2>&1 | tail -1
