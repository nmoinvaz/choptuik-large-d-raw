#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_corner_r249 || exit 1
[ "$(systemctl --user is-active i1076r249)" = active ] && { echo "i1076r249 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076r249 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076r249 bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076r249.log $PWD/lane_r249.sh full 2>&1 | tail -1
