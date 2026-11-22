#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc71_d1925 || exit 1
[ "$(systemctl --user is-active i1025k)" = active ] && { echo "i1025k active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025k --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025k bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025k.log $PWD/lane_kc71_1925.sh 2>&1 | tail -1
