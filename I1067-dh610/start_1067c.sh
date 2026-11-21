#!/bin/bash
# #1067 (dh610): starts unit i1067c (run1067_resume.sh) with the alert-only memory log
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 1
[ "$(systemctl --user is-active i1067b)" = active ] && { echo "i1067a active: not started"; exit 1; }
[ "$(systemctl --user is-active i1067c)" = active ] && { echo "i1067c active: not started"; exit 1; }
[ -e stage1_resume1.log ] && { echo "stage1_resume1.log exists: not started"; exit 1; }
[ -f ~/Source/choptuik-large-d-1067/hp/data/lowD_states/lowD1067_D3.0475_M512_ckpt.npz ] || { echo "the checkpoint is missing"; exit 1; }
date -u '+%F %T start'
systemd-run --user --unit=i1067c --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=i1067c bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_i1067c.log $PWD/run1067_resume.sh 2>&1 | tail -1
