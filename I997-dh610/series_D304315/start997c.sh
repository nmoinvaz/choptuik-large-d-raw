#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I997-dh610/series_D304315 || exit 1
[ "$(systemctl --user is-active i997s)" = active ] && { echo "i997s active"; exit 1; }
[ -e exits_997c.txt ] && { echo "exits_997c.txt exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i997s --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i997s bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i997s.log $PWD/run997c.sh 2>&1 | tail -1
