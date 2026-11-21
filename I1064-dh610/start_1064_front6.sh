#!/bin/bash
# #1064 front test (21 Nov): extracts dh370's base and jet from origin/main into the live raw clone (blob-checked, untracked) and starts unit i1064q (run1064_front6.sh)
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064t i1064u; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
[ -e front_D262.7908/a5_basepolish0 ] && { echo "front_D262.7908/a5_basepolish0 exists: not started"; exit 1; }
R=~/Source/choptuik-large-d-raw; D=I966-dh370/ks_chain3b/leg14_D261.1415_ks293
for f in anm_pin3_D262.7908.npz jet_pin3_D262.7908.npz; do
  [ -f $R/$D/$f ] || git -C $R show origin/main:$D/$f > $R/$D/$f
done
[ "$(git hash-object $R/$D/anm_pin3_D262.7908.npz)" = d15cb96c37f580a848328d29c2f69f4d121fc057 ] || { echo "state blob wrong"; exit 1; }
[ "$(git hash-object $R/$D/jet_pin3_D262.7908.npz)" = 287f4d70e93e61026bf580573c152be57090677e ] || { echo "jet blob wrong"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1064u --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1064u bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1064u.log $PWD/run1064_front6.sh 2>&1 | tail -1
