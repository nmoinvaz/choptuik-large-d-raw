#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~16:44 UTC, quoted): "report D 22.8125's signs from 0.110 to 0.400 (all scans merged) in one line. Then: extend D 22.8125 up, 0.42 to 0.50 by 0.02 (plus a repeat), to find F; and release the D 22.75
# both-roots scan (-0.10..0.50), which runs regardless. Do not label 22.8125 until F is found." The earlier order stands after them: D 22.5 and D 22.625 on 0.04 (16 points + a repeat), 22.6875, 22.5625 and 22.375 skipped.
# Same steps as post23_scans3/4 (mkF.py setup, pipeline87_rescan.sh, mkF.py read, label_roots.py, push, hc), but a reading that label_roots.py does not accept (not exactly two changes '- to +' then '+ to -') is reported and not
# labeled, and the next scan still runs. A label that succeeds takes its D out of L_ONLY.txt (mkF.py does not use those D's roots87 lines as F roots).
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans5: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stopp() { tell "macm3 #1025 post23_scans5 STOP: $*; the hold stays, nothing further is scanned"; exit 1; }
cd $L || exit 9
python3 ext23.py selftest > /dev/null 2>&1 || stopp "ext23.py selftest fails"
python3 label_roots.py selftest > /dev/null 2>&1 || stopp "label_roots.py selftest fails"
for m in swap replace; do python3 label_roots.py selftest --mutate=$m > /dev/null 2>&1 && stopp "label_roots.py selftest --mutate=$m passed (it must fail)"; done
python3 mkF.py selftest > /dev/null 2>&1 || stopp "mkF.py selftest fails"
python3 mkF.py selftest --mutate=grid > /dev/null 2>&1 && stopp "mkF.py selftest --mutate=grid passed (it must fail)"
say "started: selftests exit 0 (ext23, label_roots, mkF), mutations swap, replace, grid exit 1"
run_scan() {   # KIND: c (D 22.8125 up), a plain D (22.75 on 0.02) or D@0.04
  kind=$1
  case $kind in c) D=22.8125;; *) D=${kind%@*};; esac
  fe=$(python3 mkF.py setup $kind) || stopp "mkF.py setup $kind failed"
  say "starting $fe"
  env NP=4 NICE=15 bash $L/pipeline87_rescan.sh $fe; say "pipeline87_rescan.sh $fe returned $?"
  [ -e $L/$fe/SCAN_DONE.txt ] || stopp "the scan $fe did not finish (see $fe/pipeline.log, $fe/steps.txt)"
  rd=$(python3 mkF.py read $kind) || stopp "mkF.py read $kind failed"
  out=$(python3 label_roots.py $D $rd); rc=$?
  say "label_roots $D: $out"
  if [ $rc = 0 ]; then
    python3 - $D <<'PY'
import sys, os
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda"); D = float(sys.argv[1]); p = L + "/L_ONLY.txt"
if os.path.exists(p):
    keep = [ln for ln in open(p).read().splitlines() if ln.startswith("#") or not any(abs(float(x) - D) < 1e-9 for x in ln.split())]
    open(p + ".tmp", "w").write("\n".join(keep) + "\n"); os.replace(p + ".tmp", p)
PY
  fi
  bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: $fe scanned, read merged, roots labeled or not" >> $LOG 2>&1; say "pushed ($?)"
  if [ $rc = 0 ]; then tell "macm3 #1025 kc87 leg2 $fe read: $out"
  else tell "macm3 #1025 kc87 leg2 $fe read, NOT labeled (no guess): $out (reading $rd); the next scan goes on"; fi
}
run_scan c; run_scan 22.75; run_scan 22.5@0.04; run_scan 22.625@0.04
tell "macm3 #1025 post23_scans5: D 22.8125 up, D 22.75 (0.02), D 22.5 and D 22.625 (0.04) are done; 22.6875, 22.5625, 22.375 skipped as ordered; the chain hold stays"
