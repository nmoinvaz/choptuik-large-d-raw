#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/d19_k95 || exit 1
[ "$(systemctl --user is-active i1025al)" = active ] && { echo "i1025al active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025al --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025al bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025al.log $PWD/lane_d19_k95_scan.sh 2>&1 | tail -1
