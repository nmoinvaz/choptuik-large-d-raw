#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_m3mp || exit 1
[ "$(systemctl --user is-active i1076b)" = active ] && { echo "i1076b active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076b --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076b bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076b.log $PWD/lane_m3mp.sh 2>&1 | tail -1
