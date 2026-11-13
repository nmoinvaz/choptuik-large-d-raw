#!/bin/bash
# #632: mu at M 64, D 5 and 6 (the issue's commands). From the root of the worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2 (the build of #621; main has
# since moved to 3c35f0cd, a multidouble bump that needs an hp rebuild, so it is not pulled), nice 10, caffeinate. The issue lets step 2 run beside the D 5 axis run
# (6 + 3 threads); here the steps run one after the other and the two axis runs together (3 + 3), to stay at 6 threads.
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I632-macm3
caffeinate -is nice -n 10 python3 -u hp/scan_hp.py $R/scan_to5.jsonl hp/data/lowD_states/lowDn_D4.0000_M64.npz 5.0 --dD 0.5 --maxdD 0.5 --kc 80 --ks 200 --threads 6 --tag m64 --attempts $R/scan_to5_attempts.jsonl > $R/scan_to5.log 2>&1
echo "scan_to5 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
[ -f $R/m64_D5.0000.npz ] || { echo "no m64_D5.0000.npz: stop" >> $R/exits.txt; exit 1; }
caffeinate -is nice -n 10 python3 -u hp/scan_hp.py $R/scan_to6.jsonl $R/m64_D5.0000.npz 6.0 --dD 0.5 --maxdD 0.5 --kc 80 --ks 200 --threads 6 --tag m64 --attempts $R/scan_to6_attempts.jsonl > $R/scan_to6.log 2>&1
echo "scan_to6 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
axis() {  # tag state
  (caffeinate -is nice -n 10 python3 -u hp/modecount_test_axis.py $2 --lo=-1.5 --hi=-0.02 --s=0 --threads=3 --out=$R/axis_$1.jsonl > $R/axis_$1.log 2>&1
   echo "axis_$1 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
}
axis D5 $R/m64_D5.0000.npz
[ -f $R/m64_D6.0000.npz ] && axis D6 $R/m64_D6.0000.npz
wait
