#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc71_d19low || exit 1
[ "$(systemctl --user is-active i1025i)" = active ] && { echo "i1025i active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025i --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025i bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025i.log $PWD/lane_kc71low.sh 2>&1 | tail -1
