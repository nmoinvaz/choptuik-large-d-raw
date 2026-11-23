#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/reconv_d1975 || exit 1
[ "$(systemctl --user is-active i1025ab)" = active ] && { echo "i1025ab active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ab --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ab bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ab.log $PWD/lane_reconv_step4.sh 2>&1 | tail -1
