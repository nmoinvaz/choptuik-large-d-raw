#!/usr/bin/env python3
"""mk_kmm2.py : makes lane_kmm2.sh of I1101-macm3/ from lane_kmm.sh (t5's widening of K4, hc 27 Nov 17:1x UTC): the same state with --kappa_mm=0.25 at lambda 0.070, 0.085, 0.160, 0.180 (the control and the scan of 0.100 to 0.145 stand),
the eight signs read on the merged scan (merge_kmm.py), the secant at tol 5e-5 on the first (lowest-lambda) robust change. Every replacement asserts its count; diff_lane_kmm2.txt is the unified diff."""
import os, subprocess
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1101-macm3/")
s = open(R + "lane_kmm.sh").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:80], s.count(old), n); s = s.replace(old, new)
lines = s.split("\n")
assert lines[1].startswith("# #1101 macm3 K4 (t5's order") and lines[5].startswith("# Stops (hc to t5)"), (lines[1][:40], lines[5][:30])
lines[1:6] = [
    "# #1101 macm3 K4w (t5's order, hc 27 Nov 17:1x UTC, after the K4 scan read all - at 0.100 to 0.145): the SAME state (R1's, l1kc127k050m3, blobs 0124dbd2 and 944a8179) with --kappa_mm=0.25 (worktree choptuik-large-d-kmm f56f91d2, d18_secant.py 2f3ee874,",
    "# ellrs unchanged) at lambda 0.070 and 0.085 (below) and 0.160 and 0.180 (above), one process of 4 Rust threads; the scan of 0.100 to 0.145 and the kappa_mm 0.5 control (bit for bit) of lane_kmm.sh stand. The eight signs are read on the merged scan (merge_kmm.py,",
    "# window (0.070, 0.180)); the secant at tol 5e-5 on the first (lowest-lambda) robust change, kappa_mm 0.25; no robust change: an hc with the eight signs and the lane ends. A second robust change is named in the hc, not run.",
    "# Stops (hc to t5): a pin or selftest that does not read as wanted, the kappa_mm steps line outside 11400 to 12000, the merge refused, an exception, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_kmm2.sh [dry]",
    "{"]
s = "\n".join(lines)
assert s.count("\n{\nset -u") == 1, "the opening brace now appears twice"
s = s.replace("\n{\n{\nset -u", "\n{\nset -u")
rep("DNC=23.0_r1k050_kmm050ctl; DNM=23.0_r1k050_kmm025; SCANC=$L/$DNC; SCANM=$L/$DNM; SEC=$K/secant", "DNM=23.0_r1k050_kmm025; DNW=23.0_r1k050_kmm025w; DNG=23.0_r1k050_kmm025m; SCANW=$L/$DNW; SCANG=$L/$DNG; SEC=$K/secant")
rep("LOG=$K/exits_kmm.txt", "LOG=$K/exits_kmm_w.txt")
rep('say() { echo "== $(stamp) UTC I1101 K4: $*"', 'say() { echo "== $(stamp) UTC I1101 K4w: $*"')
rep('tell "macm3 #1101 K4 STOP: $*"', 'tell "macm3 #1101 K4w STOP: $*"')
# replace everything from the control (4) to the end
i4 = s.index("# 4. the control:")
new_tail = '''# 4. the scan of the same state at kappa_mm 0.25, lambda 0.070 0.085 0.160 0.180
[ -s $L/$DNM/scan/scan_D23.0_1025.jsonl ] && [ -s $K/control_compare.txt ] || stop "the K4 scan or its control comparison is missing"
prep_folder $DNW 0.25 '"0.070" "0.085" "0.160" "0.180"' "0.070 0.180"
say "scan starts: kappa_mm 0.25 at lambda 0.070 0.085 0.160 0.180, 1 process, 4 Rust threads (pointkmm.sh $DNW scan); the control of K4 (kappa_mm 0.5, bit for bit, kmm025/control_compare.txt) stands"
tell "macm3 #1101 K4w START: the widening starts now: the same state with --kappa_mm=0.25 at lambda 0.070, 0.085, 0.160, 0.180 (1 process of 4 Rust threads, about 30 min), then the eight signs on the merged scan and the secant at tol 5e-5 on the first robust change"
bash $F/pointkmm.sh $DNW scan >> $SCANW/pipeline.log 2>&1 &
sp=$!
n=0; until grep -q '^kappa_mm' $SCANW/scan/scan_p0.log 2>/dev/null; do n=$((n+1)); [ $n -gt 120 ] && break; kill -0 $sp 2>/dev/null || break; sleep 5; done
KL=$(grep -h '^kappa_mm' $SCANW/scan/scan_p0.log 2>/dev/null | head -1); say "scan's line: $KL"
KS=$(echo "$KL" | sed -E 's/.*, ([0-9]+) steps \\(the record.*/\\1/')
if ! python3 -c "import sys; sys.exit(0 if 11400 <= int('$KS') <= 12000 else 1)" 2>/dev/null; then pkill -f "d18_secant.py scan.*$DNW" 2>/dev/null; wait $sp; stop "the kappa_mm 0.25 steps line does not read about 11700 (11400 to 12000): '$KL'"; fi
wait $sp
say "scan exit $?"
[ -e $SCANW/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCANW/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DNW (I1101 K4w, kappa_mm 0.25, lambda 0.070 0.085 0.160 0.180) scan done" > /dev/null 2>&1
# the merged scan of the eight lambda and its reading (merge_kmm.py with its two failing mutations)
$PY $F/merge_kmm.py $DNG $DNM $DNW > $K/merge_kmm.txt 2>&1; mg=$?; $PY $F/merge_kmm.py ${DNG}_mut $DNM $DNW --mutate=dup > /dev/null 2>&1; m1=$?; $PY $F/merge_kmm.py ${DNG}_mut $DNM $DNW --mutate=steps > /dev/null 2>&1; m2=$?
say "merge exit $mg (0 wanted), its mutations dup exit $m1, steps exit $m2 (1 wanted each): $(tail -1 $K/merge_kmm.txt | cut -c1-300)"
[ $mg = 0 ] && [ $m1 = 1 ] && [ $m2 = 1 ] || stop "the merge of the two scans or its controls did not read as wanted ($mg $m1 $m2)"
mv $L/${DNG}_mut $L/${DNG}_mut.removed.$(date +%s) 2>/dev/null
cd $L/common/in
$PY -I read_lower.py selftest > $SCANG/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $SCANG/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $SCANG/selftest_read_lower_round2.txt 2>&1; e2=$?
say "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] || stop "read_lower's selftest or its mutations did not read as wanted ($e0 $e1 $e2)"
{ echo "== window: read_lower.py scan 0.070 0.180 (merged: $DNM and $DNW)"; $PY -I read_lower.py $SCANG/scan 0.070 0.180; echo "(exit $?)"; } > $SCANG/read_lower.txt 2>&1
cd $F
cp $SCANG/read_lower.txt $K/read_lower_merged.txt
SIGNS=$(grep -h '^hybrid signs' $SCANG/read_lower.txt | head -1)
nch=$(grep -c 'robust change (' $SCANG/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCANG/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint|^float64|not noise-robust' $SCANG/read_lower.txt | tr '\\n' ' ' | cut -c1-1200)"
bash $F/push_i1101.sh "I1101-macm3: K4w scan (0.070 0.085 0.160 0.180) read, merged with K4's" > /dev/null 2>&1
bash $L/push87.sh "kc87_leg_lambda: D $DNG (I1101 K4w merged reading)" > /dev/null 2>&1
tell "macm3 #1101 K4w: the eight signs at --kappa_mm=0.25 (merged scan, lambda 0.070 to 0.180): $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint|not noise-robust' $SCANG/read_lower.txt | tr '\\n' ';' | cut -c1-1100) (raw kc87_leg_lambda/$DNG/)"
if [ "$nch" = 0 ]; then tell "macm3 #1101 K4w: no robust change in 0.070 to 0.180 at --kappa_mm=0.25 ($SIGNS): no secant; the lane ends and waits for your word"; exit 0; fi
# 5. the secant on the FIRST (lowest-lambda) robust change
BR=$(grep 'robust change (' $SCANG/read_lower.txt | head -1 | sed -E 's/.*robust change \\((-?[0-9.]+), (-?[0-9.]+)\\).*/\\1 \\2/')
LO=${BR% *}; HI=${BR#* }
[ "$nch" = 1 ] || tell "macm3 #1101 K4w: $nch robust changes in 0.070 to 0.180; the secant runs on the first (lowest lambda, bracket $LO $HI), the others are not run"
S_STATE=$SCANW/in/$STATEFILE; S_REC=$SCANW/in/$TAG.jsonl
'''
j6 = s.index("mkdir -p $SEC; [ -e $SEC/secant.jsonl ]")
s = s[:i4] + new_tail + s[j6:]
rep('say "secant starts: d18_secant.py run', 'say "secant starts: d18_secant.py run')
rep("(raw I1101-macm3/kmm025/ and kc87_leg_lambda/$DNM/)", "(raw I1101-macm3/kmm025/ and kc87_leg_lambda/$DNW/)")
rep('tell "macm3 #1101 K4 done: $CMPR;', 'tell "macm3 #1101 K4w done ($(grep -h "^hybrid signs" $SCANG/read_lower.txt | head -1)): $CMPR;')
rep('$PY $F/summarize_point.py $SCANM $SEC > $K/point_summary.txt 2>&1', '$PY $F/summarize_point.py $SCANG $SEC > $K/point_summary_w.txt 2>&1')
rep("RT=$(grep -o 'det-linear root [0-9.-]*' $K/point_summary.txt", "RT=$(grep -o 'det-linear root [0-9.-]*' $K/point_summary_w.txt")
rep("$(grep -E '^(scan:|secant: status|secant root)' $K/point_summary.txt", "$(grep -E '^(scan:|secant: status|secant root)' $K/point_summary_w.txt")
rep('bash $F/push_i1101.sh "I1101-macm3: K4 scanned at kappa_mm 0.25 and its root refined (secant)"', 'bash $F/push_i1101.sh "I1101-macm3: K4w secant at kappa_mm 0.25 done"')
rep("pgrep -f \"d18_secant.py run.*I1101-macm3/kmm025/secant\"", "pgrep -f \"d18_secant.py run.*I1101-macm3/kmm025/secant\"")
open(R + "lane_kmm2.sh", "w").write(s)
d = subprocess.run(["diff", "-u", R + "lane_kmm.sh", R + "lane_kmm2.sh"], capture_output=True, text=True).stdout
open(R + "diff_lane_kmm2.txt", "w").write(d); print("lane_kmm2.sh written; diff lines:", len(d.splitlines()))
