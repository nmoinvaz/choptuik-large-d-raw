#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc95_d2175 || exit 1
[ "$(systemctl --user is-active i1025-kc95-21_75)" = active ] && { echo "i1025-kc95-21_75 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025-kc95-21_75 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025-kc95-21_75 bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025-kc95-21_75.log $PWD/lane_kc95.sh 2>&1 | tail -1
