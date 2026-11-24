#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1081-dh610 || exit 1
[ "$(systemctl --user is-active i1081)" = active ] && { echo "i1081 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1081 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1081 bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1081.log $PWD/lane_1081.sh 2>&1 | tail -1
