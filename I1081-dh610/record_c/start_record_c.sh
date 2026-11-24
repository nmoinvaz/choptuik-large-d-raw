#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1081-dh610/record_c || exit 1
[ "$(systemctl --user is-active i1081rc)" = active ] && { echo "i1081rc active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1081rc --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1081rc bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1081rc.log $PWD/run_record_c.sh 2>&1 | tail -1
