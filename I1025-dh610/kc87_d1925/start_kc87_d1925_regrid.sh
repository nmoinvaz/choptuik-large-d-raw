#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_d1925 || exit 1
[ "$(systemctl --user is-active i1025r)" = active ] && { echo "i1025r active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025r --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025r bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025r.log $PWD/lane_kc87_d1925_regrid.sh 2>&1 | tail -1
