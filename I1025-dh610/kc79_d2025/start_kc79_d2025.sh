#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_d2025 || exit 1
[ "$(systemctl --user is-active i1025af)" = active ] && { echo "i1025af active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025af --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025af bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025af.log $PWD/lane_kc79_d2025.sh 2>&1 | tail -1
