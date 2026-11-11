#!/bin/bash
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I493-macm3
raw=../choptuik-large-d-raw-push
caffeinate -is nice -n 10 python3 -u hp/near_null.py $raw I489-mac/renode_L1_horizon_D242.3642.npz --threads=2 --json=$out/near_null_L1.json > $out/near_null_L1.log 2>&1
rc=$?
echo "near_null exit $rc at $(date -u +%FT%TZ)" >> $out/exits.txt
if [ $rc -eq 0 ]; then
    caffeinate -is nice -n 10 python3 -u hp/near_null.py $raw I489-mac/renode_L1_horizon_D242.3642.npz --threads=2 --mutate=sigma > $out/near_null_L1_ctl_sigma.log 2>&1
    echo "control sigma exit $? (must be nonzero) at $(date -u +%FT%TZ)" >> $out/exits.txt
fi
