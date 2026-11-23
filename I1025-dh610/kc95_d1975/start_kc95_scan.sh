#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc95_d1975 || exit 1
[ "$(systemctl --user is-active i1025w)" = active ] && { echo "i1025w active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025w --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025w bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025w.log $PWD/lane_kc95_scan.sh 2>&1 | tail -1
