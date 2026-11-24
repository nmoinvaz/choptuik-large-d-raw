#!/bin/bash
# start_m3.sh: systemd user unit i1025-m3pts running chain_m3.sh under systemd-inhibit with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1025-dh610/kc87_m3pts || exit 1
[ "$(systemctl --user is-active i1025-m3pts)" = active ] && { echo "i1025-m3pts active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025-m3pts --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025-m3pts bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025-m3pts.log $PWD/chain_m3.sh 2>&1 | tail -1
