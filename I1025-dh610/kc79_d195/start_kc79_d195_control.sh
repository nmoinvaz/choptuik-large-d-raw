#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_d195 || exit 1
[ "$(systemctl --user is-active i1025n)" = active ] && { echo "i1025n active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025n --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025n bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025n.log $PWD/lane_kc79_d195_control.sh 2>&1 | tail -1
