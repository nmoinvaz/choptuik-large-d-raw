#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_d195 || exit 1
[ "$(systemctl --user is-active i1025p)" = active ] && { echo "i1025p active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025p --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025p bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025p.log $PWD/lane_kc87_regrid.sh 2>&1 | tail -1
