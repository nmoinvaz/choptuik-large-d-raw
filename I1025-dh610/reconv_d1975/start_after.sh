#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/reconv_d1975 || exit 1
[ "$(systemctl --user is-active i1025aa)" = active ] && { echo "i1025aa active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025aa --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025aa bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025aa.log $PWD/lane_reconv_after.sh 2>&1 | tail -1
