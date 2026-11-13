#!/bin/bash
# #621: the test-field rate mu(D) at D 4, 5, 6 and 8.25 (the coordinator's comment of 2026-11-13 01:44 UTC on the issue). From the root of the
# worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2, nice 10, caffeinate. Step 1: scan_hp.py continues the D 4 11-node M 48 state to D 6 (6 threads).
# Step 2: modecount_test_axis.py on four states, two at a time, 3 threads each.
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I621-macm3
caffeinate -is nice -n 10 python3 -u hp/scan_hp.py $R/scan_D4to6.jsonl hp/data/lowD_states/lowDn_D4.0000_M48.npz 6.0 --dD 0.5 --maxdD 0.5 --kc 80 --ks 200 --threads 6 --tag i621 --attempts $R/scan_attempts.jsonl > $R/scan_D4to6.log 2>&1
echo "scan_D4to6 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
axis() {  # tag state
  (caffeinate -is nice -n 10 python3 -u hp/modecount_test_axis.py $2 --lo=-1.5 --hi=-0.02 --s=0 --threads=3 --out=$R/axis_$1.jsonl > $R/axis_$1.log 2>&1
   echo "axis_$1 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
}
axis D4_control hp/data/lowD_states/lowDn_D4.0000_M48.npz
[ -f $R/i621_D5.0000.npz ] && axis D5 $R/i621_D5.0000.npz
wait
[ -f $R/i621_D6.0000.npz ] && axis D6 $R/i621_D6.0000.npz
axis D8.25 hp/data/states/up_D8.2500.npz
wait
