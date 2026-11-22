#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/d19125 || exit 1
[ "$(systemctl --user is-active i1025g)" = active ] && { echo "i1025g active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025g --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025g bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025g.log $PWD/lane_d19125.sh 2>&1 | tail -1
