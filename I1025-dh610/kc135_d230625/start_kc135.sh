#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc135_d230625 || exit 1
[ "$(systemctl --user is-active i1025-kc135-230625)" = active ] && { echo "i1025-kc135-230625 active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025-kc135-230625 --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025-kc135-230625 bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025-kc135-230625.log $PWD/lane_kc135.sh 2>&1 | tail -1
