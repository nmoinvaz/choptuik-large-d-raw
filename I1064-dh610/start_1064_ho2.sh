#!/bin/bash
# #1064, the coordinator's approval (21 Nov): the D 237.7132 run again with --od_floor_delta 0 (run1064g.sh, main 276aa1cd): the control ks 307 alone, then ks331 and ks347 side by side; unit i1064o, folder ho2_D237.7132/
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064k i1064l i1064m i1064n i1064o; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
[ -e ho2_D237.7132 ] && { echo "ho2_D237.7132 exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064o --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064o bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064o.log $PWD/run1064g.sh 2>&1 | tail -1
