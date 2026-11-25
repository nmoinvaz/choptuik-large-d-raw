#!/bin/bash
# #1025 macm3 (t5's order, hc 25 Nov after 14:27 UTC): the wide check of D 22.875 right after the scan of D 22.8125, before D 22.75.
# Waits (2 s polls) until no pipeline87_post23.sh for D 22.8125 runs and the scan of D 22.8125 is done, then takes the scan lock at once (pipeline87_rescan.sh), so that D 22.75's pipeline (started by post23_scans2.sh
# after the root of D 22.8125 is recorded) waits behind it. Then reads the scan alone and merged with the first scan (ext23.read_merged; D 22.875/read_lower.txt is not touched), pushes, tells t5.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC wide875: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
cd $L || exit 9
say "waiting for the scan of D 22.8125 to end"
while [ ! -e $L/22.8125/SCAN_DONE.txt ] || pgrep -f "pipeline87_post23.sh 22.8125 " > /dev/null; do sleep 2; done
say "D 22.8125's pipeline is done: starting the wide check of D 22.875"
bash $L/pipeline87_rescan.sh 22.875_wide; say "pipeline87_rescan.sh 22.875_wide returned $?"
[ -e $L/22.875_wide/SCAN_DONE.txt ] || { tell "macm3 #1025 wide875 STOP: the wide scan of D 22.875 did not finish (see 22.875_wide/pipeline.log, steps.txt)"; exit 1; }
python3 - <<'PY' >> $LOG 2>&1
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
import ext23
L = ext23.L
t = ext23.read_merged([L + "/22.875/scan", L + "/22.875_wide/scan"], L + "/22.875_wide/merged", "22.875", -0.10, 0.30)
open(L + "/22.875_wide/read_lower_merged.txt", "w").write(t)
print("merged reading written")
PY
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D 22.875 wide check scanned and read merged" >> $LOG 2>&1; say "pushed ($?)"
tell "macm3 #1025 wide875: the wide scan of D 22.875 is done and pushed ($(date -u '+%H:%M') UTC); reading in 22.875_wide/read_lower.txt (alone) and read_lower_merged.txt (with the first scan); I will score it against (C), (R) and the third reading"
