#!/bin/bash
# start_compare.sh D: systemd user unit i1025-cmp-<D> running wait_compare.sh D under systemd-inhibit with the alert-only memory log
D=$1; U=i1025-cmp-${D//./_}
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_far || exit 1
[ "$(systemctl --user is-active $U)" = active ] && { echo "$U active"; exit 1; }
mkdir -p D$D
date -u '+%F %T start'
systemd-run --user --unit=$U --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$U bash $PWD/../../I967-dh610/withmem967.sh $PWD/D$D/memlog_$U.log $PWD/wait_compare.sh $1 2>&1 | tail -1
