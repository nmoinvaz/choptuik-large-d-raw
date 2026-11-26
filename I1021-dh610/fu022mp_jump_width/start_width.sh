#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1021-dh610/fu022mp_jump_width || exit 1
[ "$(systemctl --user is-active i1076wid)" = active ] && { echo "i1076wid active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1076wid --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1076wid bash $HOME/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh $PWD/logs/memlog_i1076wid.log $PWD/lane_width.sh full 2>&1 | tail -1
