#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I997-dh610/series_D304315_r2 || exit 1
[ "$(systemctl --user is-active i997t)" = active ] && { echo "i997t active"; exit 1; }
[ -e exits_997d.txt ] && { echo "exits_997d.txt exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i997t --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i997t bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i997t.log $PWD/run997d.sh 2>&1 | tail -1
