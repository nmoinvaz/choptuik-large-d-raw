#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/d1909 || exit 1
[ "$(systemctl --user is-active i1025f)" = active ] && { echo "i1025f active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025f --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025f bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025f.log $PWD/lane_d1909.sh 2>&1 | tail -1
