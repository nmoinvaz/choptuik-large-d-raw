#!/bin/bash
# start_scan_after.sh D CENTER PRED: systemd user unit i1025-scan-<D> running scan_after_compare.sh under systemd-inhibit with the alert-only memory log
D=$1; U=i1025-scan-${D//./_}
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc79_far || exit 1
[ "$(systemctl --user is-active $U)" = active ] && { echo "$U active"; exit 1; }
mkdir -p D$D/i
date -u '+%F %T start'
systemd-run --user --unit=$U --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$U bash $PWD/../../I967-dh610/withmem967.sh $PWD/D$D/i/memlog_$U.log $PWD/scan_after_compare.sh $1 $2 $3 2>&1 | tail -1
