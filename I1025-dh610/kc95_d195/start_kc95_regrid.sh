#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc95_d195 || exit 1
[ "$(systemctl --user is-active i1025t)" = active ] && { echo "i1025t active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025t --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025t bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025t.log $PWD/lane_kc95_regrid.sh 2>&1 | tail -1
