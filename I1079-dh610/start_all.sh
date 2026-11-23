#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1079-dh610 || exit 1
[ "$(systemctl --user is-active i1079dh)" = active ] && { echo "i1079dh active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1079dh --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1079dh bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1079dh.log $PWD/run_all.sh 2>&1 | tail -1
