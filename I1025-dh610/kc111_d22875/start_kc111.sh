#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc111_d22875 || exit 1
[ "$(systemctl --user is-active i1025-kc111-22875)" = active ] && { echo "i1025-kc111-22875 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025-kc111-22875 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025-kc111-22875 bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025-kc111-22875.log $PWD/lane_kc111.sh 2>&1 | tail -1
