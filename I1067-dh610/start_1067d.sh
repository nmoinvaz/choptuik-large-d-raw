#!/bin/bash
# #1067 (dh610): starts unit i1067d (run1067_call4.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 1
[ "$(systemctl --user is-active i1067c)" = active ] && { echo "i1067a active: not started"; exit 1; }
[ "$(systemctl --user is-active i1067d)" = active ] && { echo "i1067d active: not started"; exit 1; }
[ -e stage1_resume3.log ] && { echo "stage1_resume3.log exists: not started"; exit 1; }
[ -f ~/Source/choptuik-large-d-1067/hp/data/lowD_states/lowD1067_D3.0475_M512_ckpt.npz ] || { echo "the checkpoint is missing"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1067d --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1067d bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1067d.log $PWD/run1067_call4.sh 2>&1 | tail -1
