#!/bin/bash
# #1064, the coordinator's re-seeded-base route: unit i1064j runs run1064d.sh (its defaults are the real run: leg 14's D 261.6229 state, control ks 293 with --reseed_base 1, then ks 315 and 294 side by side, 7200 s caps)
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
[ "$(systemctl --user is-active i1064j)" = active ] && { echo "i1064j already active"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064j --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064j bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064j.log $PWD/run1064d.sh 2>&1 | tail -1
