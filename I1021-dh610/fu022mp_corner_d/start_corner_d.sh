#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_corner_d || exit 1
[ "$(systemctl --user is-active i1076cd)" = active ] && { echo "i1076cd active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076cd --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076cd bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076cd.log $PWD/lane_corner_d.sh full 2>&1 | tail -1
