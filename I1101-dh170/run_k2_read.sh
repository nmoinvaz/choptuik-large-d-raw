#!/bin/bash
# #1101 Test K extension, after t5's order of 17:4x UTC 27 Nov ("let the four scan points finish for the record, but do NOT run its secant"): the read-only stages of run_scan_k2.sh,
# run by hand when the four scans have ended (the driver was frozen with SIGSTOP at 17:44:45 UTC so that its secant stage cannot start; its unit is stopped before this script, t5's order).
# Writes read_lower_k2.txt and results_k2.md (the eight points); no secant; DONE_k2.txt. Stops at the first failure (STOP_k2r.txt).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=k2r
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
n=$(grep -c '\[k2\] lambda .* exit 0' steps.txt)
[ "$n" = 4 ] || stop "$n of the four scans exited 0"
for f in scan_k2_p*.raw; do grep -h 'the record system\|NOT the record system\|block 12 by ellrs\|^kappa_mm' $f | head -4 >> steps.txt; grep -hE 'Elapsed|Maximum resident' $f >> steps.txt; done
grep -l 'NOT the record system' scan_k2_p*.raw && stop "a scan did not reproduce the record system"
[ "$(ls scan_k/scan_D23.0_p*.jsonl | wc -l)" = 8 ] || stop "the eight scan files are not all there"
( cd in; { echo "== k2: read_lower.py scan_k 0.040 0.150"; $PY -I read_lower.py $OUT/scan_k 0.040 0.150; echo "(exit $?)"; } > $OUT/read_lower_k2.txt 2>&1 )
$PY -I results_1101k.py scan scan_k > results_k2.md 2> results_k2.err; rc=$?
step "results_1101k.py scan (eight points) exit $rc (2 no robust change, 3 a bracket; no secant, t5's order), results_k2.md"
echo "k2 DONE $(stamp) UTC, scans only: no secant (t5's order); reading exit $rc" > DONE_k2.txt
step "done"
exit 0
}
