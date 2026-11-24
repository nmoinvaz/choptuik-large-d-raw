#!/bin/bash
# start_k87.sh D CENTER PRED: systemd user unit i1025-k87l-<D> (D with _ for .) running wait_k87.sh under systemd-inhibit with the alert-only memory log
D=$1; U=i1025-k87l-${D//./_}
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_leg_lambda || exit 1
[ "$(systemctl --user is-active $U)" = active ] && { echo "$U active"; exit 1; }
mkdir -p $D
date -u '+%F %T start'
systemd-run --user --unit=$U --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$U bash $PWD/../../I967-dh610/withmem967.sh $PWD/$D/memlog_$U.log $PWD/wait_k87.sh $1 $2 $3 2>&1 | tail -1
