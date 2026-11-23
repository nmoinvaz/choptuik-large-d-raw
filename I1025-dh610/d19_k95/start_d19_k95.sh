#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/d19_k95 || exit 1
[ "$(systemctl --user is-active i1025ak)" = active ] && { echo "i1025ak active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ak --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ak bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ak.log $PWD/lane_d19_k95.sh 2>&1 | tail -1
