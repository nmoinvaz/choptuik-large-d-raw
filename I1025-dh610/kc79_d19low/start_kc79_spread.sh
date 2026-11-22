#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_d19low || exit 1
[ "$(systemctl --user is-active i1025l)" = active ] && { echo "i1025l active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025l --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025l bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025l.log $PWD/lane_kc79_spread.sh 2>&1 | tail -1
