#!/bin/bash
# #1064, the coordinator's order (21 Nov): K = 395 and 443 side by side from the ks 307 base at D 237.7132 (run1064h.sh, main 276aa1cd); unit i1064p, folder ho3_D237.7132/
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064k i1064l i1064m i1064n i1064o i1064p; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
[ -e ho3_D237.7132 ] && { echo "ho3_D237.7132 exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064p --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064p bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064p.log $PWD/run1064h.sh 2>&1 | tail -1
