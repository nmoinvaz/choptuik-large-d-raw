#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_jump_map || exit 1
[ "$(systemctl --user is-active i1076map)" = active ] && { echo "i1076map active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076map --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076map bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076map.log $PWD/lane_map.sh full 2>&1 | tail -1
