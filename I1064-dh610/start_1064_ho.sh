#!/bin/bash
# #1064, the coordinator's follow-on (21 Nov): the largest order a polish reaches at D 237.7132 (run1064f.sh, main 276aa1cd): the control ks 307 alone, then ks331 and ks347 side by side
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064k i1064l i1064m i1064n; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
[ -e ho_D237.7132 ] && { echo "ho_D237.7132 exists: not started"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064n --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064n bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064n.log $PWD/run1064f.sh 2>&1 | tail -1
