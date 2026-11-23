#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_d205 || exit 1
[ "$(systemctl --user is-active i1025ah)" = active ] && { echo "i1025ah active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ah --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ah bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ah.log $PWD/lane_kc87_d205.sh 2>&1 | tail -1
