#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~16:50 UTC, quoted in mkF.py kind d/e): leave every label as is until D 22.75's both-roots scan reads (LABELS_FROZEN.txt: label_roots.py writes nothing while it exists);
# then D 22.9375 on -0.50..-0.10 by 0.04 (the lower track's position) and D 22.875 on 0.30..0.50 by 0.04; then, as ordered before, D 22.5 and D 22.625 on 0.04 (22.6875, 22.5625, 22.375 skipped).
# Replaces post23_scans6.sh (killed ~18:27 UTC while its 22.9375_low scan ran): t5 (hc ~18:25 UTC) put D 23.0 on -0.50..-0.10 by 0.04 right after D 22.9375_low, before D 22.875_up. Waits for 22.9375_low, reads it (frozen: not labeled), then f, e, 22.5@0.04, 22.625@0.04.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans7: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stopp() { tell "macm3 #1025 post23_scans7 STOP: $*; the hold stays, nothing further is scanned"; exit 1; }
cd $L || exit 9
python3 ext23.py selftest > /dev/null 2>&1 || stopp "ext23.py selftest fails"
python3 label_roots.py selftest > /dev/null 2>&1 || stopp "label_roots.py selftest fails"
for m in swap replace freeze; do python3 label_roots.py selftest --mutate=$m > /dev/null 2>&1 && stopp "label_roots.py selftest --mutate=$m passed (it must fail)"; done
python3 mkF.py selftest > /dev/null 2>&1 || stopp "mkF.py selftest fails"
python3 mkF.py selftest --mutate=grid > /dev/null 2>&1 && stopp "mkF.py selftest --mutate=grid passed (it must fail)"
say "started: selftests exit 0 (ext23, label_roots, mkF), mutations swap, replace, freeze, grid exit 1"
finish_scan() {   # KIND
  kind=$1
  case $kind in c) D=22.8125;; d) D=22.9375;; e) D=22.875;; f) D=23.0;; *) D=${kind%@*};; esac
  fe=$(python3 mkF.py folder $kind)
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
  bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: $fe scanned and read merged" >> $LOG 2>&1; say "pushed ($?)"
  sg=$(grep -h 'hybrid signs\|robust change (\|robust changes' $rd | sed 's/^ *//' | tr '\n' ';' | cut -c1-900)
  tell "macm3 #1025 kc87 leg2 $fe read ($(date -u '+%H:%M') UTC; labels: $(echo "$out" | cut -c1-120)): $sg"
}
run_scan() {
  kind=$1
  fe=$(python3 mkF.py setup $kind) || stopp "mkF.py setup $kind failed"
  say "starting $fe"
  env NP=4 NICE=15 bash $L/pipeline87_rescan.sh $fe; say "pipeline87_rescan.sh $fe returned $?"
  finish_scan $kind
}
say "waiting for the running scan 22.9375_low (pipeline87_rescan.sh 22.9375_low)"
while pgrep -f "pipeline87_rescan.sh 22.9375_low" > /dev/null; do sleep 10; done
finish_scan d
run_scan f; run_scan e; run_scan 22.5@0.04; run_scan 22.625@0.04
tell "macm3 #1025 post23_scans7: D 22.9375 low, D 23.0 low, D 22.875 up, D 22.5 and D 22.625 (0.04) are done; the chain hold stays; labels were frozen throughout"
