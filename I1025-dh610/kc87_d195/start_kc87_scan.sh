#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_d195 || exit 1
[ "$(systemctl --user is-active i1025q)" = active ] && { echo "i1025q active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025q --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025q bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025q.log $PWD/lane_kc87_scan.sh 2>&1 | tail -1
