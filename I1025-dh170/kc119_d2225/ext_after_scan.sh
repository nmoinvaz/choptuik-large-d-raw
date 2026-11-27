#!/bin/bash
# #1025 kc119_d2225 (t5's hc 27 Nov 02:11 UTC): waits for SCAN_DONE.txt (the original scan, the repeat of 0.04 included, has ended), then runs run_scan_ext.sh (lambda -0.06, -0.08, -0.10, nice 19).
# Polls each 60 s, for at most 20 h; the exit code goes to exits_k119.txt. A systemd user unit.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc119_d2225
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
echo "$(stamp) UTC ext_after_scan.sh waits for SCAN_DONE.txt" >> $OUT/steps.txt
for i in $(seq 1 1200); do [ -e $OUT/SCAN_DONE.txt ] && break; sleep 60; done
[ -e $OUT/SCAN_DONE.txt ] || { echo "$(stamp) UTC EXT STOP: SCAN_DONE.txt did not appear in 20 h" >> $OUT/steps.txt; exit 1; }
echo "$(stamp) UTC SCAN_DONE.txt exists: starting run_scan_ext.sh" >> $OUT/steps.txt
bash $OUT/run_scan_ext.sh; rc=$?
echo "ext $rc" >> $OUT/exits_k119.txt
exit 0
}
