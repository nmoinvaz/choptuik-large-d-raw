#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/reconv_d1975 || exit 1
[ "$(systemctl --user is-active i1025z)" = active ] && { echo "i1025z active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025z --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025z bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1025z.log $PWD/lane_reconv_refine.sh mac 2>&1 | tail -1
