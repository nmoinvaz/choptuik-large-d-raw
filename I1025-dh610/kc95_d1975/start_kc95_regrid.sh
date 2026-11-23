#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc95_d1975 || exit 1
[ "$(systemctl --user is-active i1025v)" = active ] && { echo "i1025v active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025v --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025v bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025v.log $PWD/lane_kc95_regrid.sh 2>&1 | tail -1
