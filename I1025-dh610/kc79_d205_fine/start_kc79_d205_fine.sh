#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_d205_fine || exit 1
[ "$(systemctl --user is-active i1025ai)" = active ] && { echo "i1025ai active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ai --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ai bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ai.log $PWD/lane_kc79_d205_fine.sh 2>&1 | tail -1
