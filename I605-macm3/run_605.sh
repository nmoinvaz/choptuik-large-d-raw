#!/bin/bash
# #605 with the coordinator's option (message of 2026-11-12 17:35 UTC): hp/modecount_qdet.py --ulps=1,2,4,8 (main 84f99e4f) at s3 (D 61, M 64, kf 23)
# and at #596's real root point (D 55.04, M 64, kf 33), each twice (the bit-equality control), 4 threads, from the worktree ~/Source/choptuik-large-d-b596
# (the modecount_cx built there from 742bb879's source, which the coordinator says still agrees with the newer main; the Python hpkernel of 2026-11-09).
cd ~/Source/choptuik-large-d-b596/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I605-macm3/started.txt
S3=$raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz
for name in s3 s3_repeat; do
    caffeinate -is nice -n 10 python3 -u modecount_qdet.py $S3 0.132000,2.912795 --M=64 --kf=23 --fmax=1e-15 --threads=4 --ulps=1,2,4,8 --json=$raw/I605-macm3/$name.json > $raw/I605-macm3/$name.log 2>&1
    echo "$name exit $? at $(date -u +%FT%TZ)" >> $raw/I605-macm3/exits.txt
done
for name in root root_repeat; do
    caffeinate -is nice -n 10 python3 -u modecount_qdet.py data/states/up10_D55.0351.npz 2.0476841270,0 --M=64 --kf=33 --fmax=1e-15 --threads=4 --ulps=1,2,4,8 --json=$raw/I605-macm3/$name.json > $raw/I605-macm3/$name.log 2>&1
    echo "$name exit $? at $(date -u +%FT%TZ)" >> $raw/I605-macm3/exits.txt
done
