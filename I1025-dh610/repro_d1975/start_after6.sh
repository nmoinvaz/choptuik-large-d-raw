#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/repro_d1975 || exit 1
[ "$(systemctl --user is-active i1025ae)" = active ] && { echo "i1025ae active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ae --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ae bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ae.log $PWD/lane_after6.sh 2>&1 | tail -1
