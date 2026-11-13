#!/bin/bash
# #621, the rest after the coordinator's reply of 2026-11-13 02:19 UTC (the continuation does not land on D 5): run_621.sh's wrapper was stopped at 02:19 UTC
# while its scan (pid 781, still running, D 5.8001 saved) went on; this script waits for that scan, then makes the one step from i621_D4.8912.npz to
# D 5.0 (the coordinator's command), then runs the four axis scans two at a time (D4 control with D5, then D6 with D8.25).
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I621-macm3
while kill -0 781 2>/dev/null; do sleep 5; done
if grep -q '^D=6.0000 ' $R/scan_D4to6.log && [ -f $R/i621_D6.0000.npz ]; then st="i621_D6.0000.npz saved"; else st="NO D 6.0000 state"; fi
echo "scan_D4to6 ended at $(date -u +%FT%TZ) (exit status not observed: its wrapper run_621.sh was stopped at 02:19 UTC; $st)" >> $R/exits.txt
caffeinate -is nice -n 10 python3 -u hp/scan_hp.py $R/scan_to5.jsonl $R/i621_D4.8912.npz 5.0 --dD 0.11 --maxdD 0.11 --kc 80 --ks 200 --threads 6 --tag i621 --attempts $R/scan_attempts_to5.jsonl > $R/scan_to5.log 2>&1
echo "scan_to5 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
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
