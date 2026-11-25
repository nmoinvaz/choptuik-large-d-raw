#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_corner_e1 || exit 1
[ "$(systemctl --user is-active i1076e1)" = active ] && { echo "i1076e1 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076e1 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076e1 bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076e1.log $PWD/lane_tiles_e1.sh full 2>&1 | tail -1
