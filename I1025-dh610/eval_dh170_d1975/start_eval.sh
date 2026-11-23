#!/bin/bash
cd ~/Source/choptuik-large-d-raw/I1025-dh610/eval_dh170_d1975 || exit 1
[ "$(systemctl --user is-active i1025ac)" = active ] && { echo "i1025ac active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1025ac --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1025ac bash $PWD/../../I967-dh610/withmem967.sh $PWD/memlog_i1025ac.log $PWD/lane_eval.sh 2>&1 | tail -1
