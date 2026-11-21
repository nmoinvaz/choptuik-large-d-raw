#!/bin/bash
# #1064, the coordinator's order (~14:45 UTC 21 Nov): the projection switch from D 262.0099 (run1064e.sh, main 276aa1cd): the control ks 293 alone, then ks315own and ks315nat side by side
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064j i1064k i1064l i1064m; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
[ -e sw_D262.0099 ] && { echo "sw_D262.0099 exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064m --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064m bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064m.log $PWD/run1064e.sh 2>&1 | tail -1
