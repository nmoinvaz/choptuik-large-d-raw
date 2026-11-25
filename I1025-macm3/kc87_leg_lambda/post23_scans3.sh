#!/bin/bash
# #1025 macm3 (t5's order, hc 25 Nov, after 15:48 UTC, quoted in mkF.py): after the running scan of D 22.75 (narrow window): (a) D 22.875 upper root F on 0.17-0.19, (b) D 22.8125 F on 0.24-0.40, then D 22.75 on -0.10 to 0.50 by 0.02;
# D 22.5 and the rest follow in a later driver (their folders and pins are not made yet). Each scan: mkF.py setup (folder, point.env, README registration first), pipeline87_rescan.sh, mkF.py read (merged reading with the earlier scans of that D),
# label_roots.py (two changes: the F line and the #L comment line of roots87.txt; anything else: STOP), push, hc to t5. The chain's pending skips these points (EXT_ORDER.txt without EXT_CLEARED.txt); no hold is released here.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans3: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stopp() { tell "macm3 #1025 post23_scans3 STOP: $*; the hold stays, nothing further is scanned"; exit 1; }
cd $L || exit 9
python3 ext23.py selftest > /dev/null 2>&1 || stopp "ext23.py selftest fails"
python3 label_roots.py selftest > /dev/null 2>&1 || stopp "label_roots.py selftest fails"
for m in swap replace; do python3 label_roots.py selftest --mutate=$m > /dev/null 2>&1 && stopp "label_roots.py selftest --mutate=$m passed (it must fail)"; done
python3 mkF.py selftest > /dev/null 2>&1 || stopp "mkF.py selftest fails"
python3 mkF.py selftest --mutate=grid > /dev/null 2>&1 && stopp "mkF.py selftest --mutate=grid passed (it must fail)"
say "started: selftests exit 0 (ext23, label_roots, mkF), mutations swap, replace, grid exit 1"
say "waiting for the narrow scan of D 22.75 (pipeline87_post23.sh 22.75) to end"
while pgrep -f "pipeline87_post23.sh 22.75 " > /dev/null; do sleep 10; done
[ -e $L/22.75/SCAN_DONE.txt ] || stopp "the narrow scan of D 22.75 did not finish (no SCAN_DONE.txt)"
say "the narrow scan of D 22.75 is done: $(grep -h 'robust change\|robust changes\|endpoint' $L/22.75/read_lower.txt | tr '\n' ';' | cut -c1-300)"
run_scan() {   # KIND (a, b or D)
  kind=$1
  case $kind in a) D=22.875;; b) D=22.8125;; *) D=$kind;; esac
  fe=$(python3 mkF.py setup $kind) || stopp "mkF.py setup $kind failed"
  say "starting $fe"
  env NP=4 NICE=15 bash $L/pipeline87_rescan.sh $fe; say "pipeline87_rescan.sh $fe returned $?"
  [ -e $L/$fe/SCAN_DONE.txt ] || stopp "the scan $fe did not finish (see $fe/pipeline.log, $fe/steps.txt)"
  rd=$(python3 mkF.py read $kind) || stopp "mkF.py read $kind failed"
  out=$(python3 label_roots.py $D $rd); rc=$?
  say "label_roots $D: $out"
  bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: $fe scanned, read merged, roots labeled" >> $LOG 2>&1; say "pushed ($?)"
  [ $rc = 0 ] || stopp "label_roots.py D $D: $out (reading $rd)"
  tell "macm3 #1025 kc87 leg2 $fe read: $out"
}
run_scan a; run_scan b; run_scan 22.75
tell "macm3 #1025 post23_scans3: (a), (b) and the D 22.75 wide scan are done; D 22.5 and the rest wait for their folders (not built yet)"
