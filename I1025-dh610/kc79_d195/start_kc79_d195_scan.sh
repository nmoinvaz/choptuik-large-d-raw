#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_d195 || exit 1
[ "$(systemctl --user is-active i1025o)" = active ] && { echo "i1025o active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025o --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025o bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025o.log $PWD/lane_kc79_d195_scan.sh 2>&1 | tail -1
