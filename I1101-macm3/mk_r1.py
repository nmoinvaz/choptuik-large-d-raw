#!/usr/bin/env python3
"""mk_r1.py : makes lane_r1.sh, push_i1101.sh, in_blobs.txt, scan_plan.env and scan_plan_ext.env of I1101-macm3/ from the files of I1025-macm3/kc143_d23125x/ (the lane of the k_c 143 cross-path check).
t5's order (hc 27 Nov 14:34 UTC, #1101 comment 7220957360): R1, winb's k_c 127 D 23.0 state (raw I1025-win/kc127_d23/, blobs 7a1b150c and eea03461) re-solved at kappa 0.5 in the 48c36355 worktree:
ell_refine.py l1kc127wind23 127 l1kc127k050m3 127 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (the lanes' threads, cap and pins); bars |F| <= 5e-10 and steps 5851 +- 2%;
then the scan at lambda 0.070, 0.085, 0.100, 0.115, 0.130 on the Rust block and the secant at tol 5e-5 on the robust change; if none brackets, 0.055 and 0.150 next, then report.
Every replacement asserts its count; the unified diff of the lane goes to diff_lane_r1.txt. Run from anywhere; writes into I1101-macm3/."""
import os, re, subprocess
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/")
B = R + "I1025-macm3/kc143_d23125x/"; X = R + "I1101-macm3/"
s = open(B + "lane_d23125x.sh").read()


def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old, s.count(old), n)
    s = s.replace(old, new)


# header: lines 3-7 (indices 2 to 6) of the old lane
lines = s.split("\n")
assert lines[2].startswith("# #1025 macm3 kc143_d23125x (t5's order") and lines[6].rstrip().endswith("usage: bash lane_d23125x.sh [dry|check]"), (lines[2][:60], lines[6][-60:])
hdr = [
    "# #1101 macm3 R1 (t5's order, hc 27 Nov 14:34 UTC and #1101 comment 7220957360): winb's k_c 127 state at D 23.0 (raw I1025-win/kc127_d23/, state 7a1b150c, record eea03461, copies in in/) RE-SOLVED AT KAPPA 0.5, tag l1kc127k050m3,",
    "# in the 48c36355 worktree (ell_refine.py 631e5801, dss_ell.py 5d28c19e): the step error of lambda_1 against kappa 0.7 (R0 root 0.045968) and R2's 0.35. Derived from kc143_d23125x/lane_d23125x.sh by mk_r1.py (diff_lane_r1.txt): the source and",
    "# destination tags, k_c 127 to 127, kappa 0.5, D 23.0, the source check (the k_c 127 check accepts winb's state, controls exit 1 1, the k_c 135 and k_c 143 checks refuse it), the bars (|F| <= 5e-10, steps 5851 +- 2%, STOP when not met),",
    "# the scan of lambda 0.070, 0.085, 0.100, 0.115, 0.130 plus a repeat of 0.070 (scan_plan.env), the extension to 0.055 and 0.150 when the window reads no robust change (scan_plan_ext.env; then a report, no secant), and an hc at the regrid's start.",
    "# Stops (hc to t5): a source or result not accepted, a bar not met, an exception (an array limit included), more than one robust change, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_r1.sh [dry|check]",
]
lines[2:7] = hdr
s = "\n".join(lines)
rep("F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125x; IN=$F/in;", "F=$HOME/Source/choptuik-large-d-raw-903/I1101-macm3; IN=$F/in;")
rep("SRC=l1kc127Lmacm3; TAG=l1kc143macm3d23125x; D=23.125; DT=D23.1250; SRCFILE=sol_${SRC}_D23.1250.npy; LAM0=2.0987860107; DN=23.125_kc143x;",
    "SRC=l1kc127wind23; TAG=l1kc127k050m3; D=23.0; DT=D23.0000; SRCFILE=sol_${SRC}_D23.0000.npy; LAM0=2.0992182200; DN=23.0_r1k050; DNX=23.0_r1k050_ext;")
rep("LOG=$F/exits_kc143.txt", "LOG=$F/exits_r1.txt")
rep('say() { echo "== $(stamp) UTC kc143_d23125x: $*" | tee -a $LOG; }', 'say() { echo "== $(stamp) UTC I1101 R1: $*" | tee -a $LOG; }')
rep('tell "macm3 #1025 kc143_d23125x STOP: $*"', 'tell "macm3 #1101 R1 STOP: $*"')
rep("SCAN=$L/$DN; SEC=$F/secant", "SCAN=$L/$DN; SCANX=$L/$DNX; SEC=$F/secant")
# the source check
rep("say \"source check (my k_c 127 state at D $D, kc127_leg): kc127_syscheck", "say \"source check (winb's k_c 127 state at D $D, I1025-win/kc127_d23, kappa 0.7): kc127_syscheck")
rep("= e1dccb3c ]", "= 7a1b150c ]")
rep('[ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 7a1b150c ] || stop "copied source state blob differs"',
    '[ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 7a1b150c ] || stop "copied source state blob differs"\n[ "$(blob $REC | cut -c1-8)" = eea03461 ] || stop "the source record blob differs"')
# the regrid: k_c 127 to 127 at kappa 0.5; the pilot hc at its start
rep("ell_refine.py $SRC 127 $TAG 143 1 $D $LAM0 --kappa 0.7 --u0 0.04", "ell_refine.py $SRC 127 $TAG 127 1 $D $LAM0 --kappa 0.5 --u0 0.04")
rep('say "regrid starts: $CMD"\n', 'say "regrid starts: $CMD"\ntell "macm3 #1101 R1 START (pilot): winb\'s k_c 127 D 23.0 state (7a1b150c, record eea03461: |F| 3.19e-10, steps 4179 at kappa 0.7) accepted by the k_c 127 check (controls 1 1, the k_c 135 and k_c 143 checks refuse it); the pins, selftests and the new scanner\'s selftests as wanted; regrid at kappa 0.5 starts now: $(echo $CMD | sed \'s/.*ell_refine.py/ell_refine.py/\'); bars |F| <= 5e-10 and steps 5851 +- 2%, 6 threads, cap 28800 s, load $(sysctl -n vm.loadavg), $(availgib) GiB available"\n')
# the result check: the k_c 127 check accepts, the k_c 135 and k_c 143 checks refuse; then t5's bars
old = s[s.index("C143=\"nice -n 10"):s.index("echo \"ACCEPTED $(stamp) UTC\" > $OUT/VERDICT.txt")]
new = '''C127R="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM"
$C127R > $OUT/syscheck.txt 2>&1; c0=$?; $C127R --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C127R --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc135check_refuses.txt 2>&1; c3=$?
nice -n 10 $PY -I $IN/kc143_syscheck_1025.py $IN/$TAG.jsonl $IN/sol_${TAG}_$DT.npy $D $WTM > $OUT/syscheck_kc143check_refuses.txt 2>&1; c4=$?
say "kc127 syscheck exit $c0 (0 wanted); controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each); kc135_syscheck on the result exit $c3, kc143_syscheck on the result exit $c4 (1 wanted each): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ $c0 = 0 ] && [ $c1 = 1 ] && [ $c2 = 1 ] && [ $c3 = 1 ] && [ $c4 = 1 ] || stop "the regrid result is not accepted (syscheck $c0, controls $c1 $c2, kc135 check on the result $c3, kc143 check on the result $c4)"
# t5's bars: |F| <= 5e-10 and steps 5851 +- 2% (5734 to 5968)
python3 - $IN/$TAG.jsonl $D <<'PY' > $OUT/bars.txt; bars=$?
import json, sys
rec = [json.loads(l) for l in open(sys.argv[1]) if l.strip() and json.loads(l)["D"] == float(sys.argv[2])][-1]
okF = rec["F"] <= 5e-10; okS = 5851 * 0.98 <= rec["steps"] <= 5851 * 1.02
print("bars: |F| %.4e <= 5e-10: %s; steps %d in [%.1f, %.1f] (5851 +- 2%%, %+.2f%%): %s" % (rec["F"], okF, rec["steps"], 5851 * 0.98, 5851 * 1.02, 100.0 * (rec["steps"] / 5851.0 - 1), okS))
sys.exit(0 if okF and okS else 1)
PY
say "$(cat $OUT/bars.txt)"
[ $bars = 0 ] || stop "a bar of t5's is not met: $(cat $OUT/bars.txt)"
'''
s = s.replace(old, new)
# summary: the record against the source (winb, kappa 0.7)
rep('print("k_c 143 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (k_c 127 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f, constraint ratio %.3f" % (',
    'print("kappa 0.5 record: D %r |F| %.4e steps %d psi-constraint %.4e Delta %.12f (winb kappa 0.7 source: |F| %.4e steps %d constraint %.4e Delta %.12f); Delta shift %+.4e, steps ratio %.3f, constraint ratio %.3f" % (')
rep('tell "macm3 #1025 kc143_d23125x: the k_c 143 D 23.125 regrid is ACCEPTED ($(cat $OUT/regrid_summary.txt)); regrid wall $(( $(date +%s) - t0 )) s; the scan ($(grep -c . $F/scan_plan.env) lines of plan, see scan_plan.env) starts now; raw $RP"',
    'tell "macm3 #1101 R1 regrid END: ACCEPTED ($(cat $OUT/regrid_summary.txt)); $(cat $OUT/bars.txt); regrid wall $(( $(date +%s) - t0 )) s; the scan of lambda 0.070 0.085 0.100 0.115 0.130 (+ the repeat of 0.070) starts now; raw $RP"')
rep('say "pushed regrid: $RP"', 'say "pushed regrid: $RP"')
rep('"kc143_d23125x: k_c 143 D 23.125 regrid accepted (state, record, checks)"', '"I1101-macm3: R1 regrid accepted (state, record, checks)"')
# the push script name and the folder names
rep("push_kc143_d23125x.sh", "push_i1101.sh", s.count("push_kc143_d23125x.sh"))
# scan folder: the raw path of the pinned inputs, the verdict text
rep("$RAWC:I1025-macm3/kc143_d23125x/in/$TAG.jsonl", "$RAWC:I1101-macm3/in/$TAG.jsonl")
rep("SRC=I1025-macm3/kc143_d23125x/in", "SRC=I1101-macm3/in")
rep('echo "ACCEPTED $(stamp) UTC (the k_c 143 regrid check of the lane, $OUT/syscheck.txt; controls and the k_c 135 refusal in $OUT)" > $SCAN/VERDICT.txt',
    'echo "ACCEPTED $(stamp) UTC (the k_c 127 check of the lane on the kappa 0.5 result, $OUT/syscheck.txt; controls and the k_c 135 and k_c 143 refusals in $OUT; t5\'s bars $OUT/bars.txt)" > $SCAN/VERDICT.txt')
rep('echo "$(stamp) UTC accept (lane_d23125.sh): kc143_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc135_syscheck on the result exit $c3 (1 wanted): $(grep -E \'^D \' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt',
    'echo "$(stamp) UTC accept (lane_r1.sh): kc127_syscheck_1025.py exit $c0 (0 wanted); controls exit $c1 $c2 (1 wanted); kc135 and kc143 checks on the result exit $c3 $c4 (1 wanted each): $(grep -E \'^D \' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt')
rep('"kc87_leg_lambda: D $DN pins and verdict (kc143 regrid of D 23.125)"', '"kc87_leg_lambda: D $DN pins and verdict (I1101 R1, kappa 0.5)"')
rep('"kc87_leg_lambda: D $DN (k_c 143) scan done"', '"kc87_leg_lambda: D $DN (I1101 R1) scan done"')
rep('tell "macm3 #1025 kc143_d23125x: the k_c 143 D 23.125 scan is read:', 'tell "macm3 #1101 R1: the scan is read:')
# the scan block (stage 6) is copied for the extension
i6 = s.index("mkdir -p $SCAN\n"); i6e = s.index("nch=$(grep -c 'robust change ('")
blk = s[i6:i6e]
assert blk.count('say "scan starts (pointnew_rs.sh $DN scan:') == 1
ext = blk.replace("$SCAN", "$SCANX").replace("$DN", "$DNX").replace("scan_plan.env", "scan_plan_ext.env")
ext = ext.replace('say "scan starts (', 'say "extension scan starts (').replace('say "scan exit $sc"', 'say "extension scan exit $sc"').replace('say "reading:', 'say "extension reading:')
ext = ext.replace('tell "macm3 #1101 R1: the scan is read:', 'tell "macm3 #1101 R1 EXTENSION (0.055 and 0.150 with 0.070 and 0.130 and a repeat of 0.055, your order when no pair brackets) scan is read:')
ext = ext.replace('"kc87_leg_lambda: D $DNX pins and verdict (I1101 R1, kappa 0.5)"', '"kc87_leg_lambda: D $DNX pins and verdict (I1101 R1 extension)"').replace('"kc87_leg_lambda: D $DNX (I1101 R1) scan done"', '"kc87_leg_lambda: D $DNX (I1101 R1 extension) scan done"')
assert "$SCAN/" not in ext.replace("$SCANX/", "") and "$DN " not in ext.replace("$DNX ", "") and "$DN\n" not in ext, "a main-scan name is left in the extension block"
branch = '''if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then
  # t5's order: no pair brackets in 0.070-0.130: scan 0.055 and 0.150 next, then report (no secant)
  tell "macm3 #1101 R1: the scan reads 0 robust changes in 0.070-0.130: the extension scan of 0.055 and 0.150 starts now (your order), then a report; no secant unless you say"
  ''' + ext.rstrip() + '''
  nchx=$(grep -c 'robust change (' $SCANX/read_lower.txt); nrbx=$(grep -o 'robust changes: [0-9]*' $SCANX/read_lower.txt | head -1 | grep -o '[0-9]*')
  say "extension reading: $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint|^repeated|^float64' $SCANX/read_lower.txt | tr '\\n' ' ' | cut -c1-900)"
  tell "macm3 #1101 R1 EXTENSION done (0.055 and 0.150 with 0.070, 0.130 and a repeat of 0.055): $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint' $SCANX/read_lower.txt | tr '\\n' ';' | cut -c1-900); the secant is not run without your word (raw I1101-macm3/ and kc87_leg_lambda/$DNX/)"
  exit 0
fi
'''
rep("[ \"$nch\" = 1 ] && [ \"$nrb\" = 1 ] || { tell \"macm3 #1025 kc143_d23125x: the scan reads $nrb robust changes (one wanted): no secant refinement; reported, the window is not widened without your word\"; exit 0; }",
    branch + "[ \"$nch\" = 1 ] && [ \"$nrb\" = 1 ] || { tell \"macm3 #1101 R1 STOP: the scan reads $nrb robust changes in 0.070-0.130 (one wanted; none goes to the extension): no secant; reported\"; exit 1; }")
# the secant
rep('pgrep -f "d18_secant.py run.*kc143_d23125x/secant"', 'pgrep -f "d18_secant.py run.*I1101-macm3/secant"')
rep('tell "macm3 #1025 kc143_d23125x done:', 'tell "macm3 #1101 R1 done:')
rep('"kc143_d23125x: D 23.125 scanned and its root refined (secant)"', '"I1101-macm3: R1 scanned and its root refined (secant)"')
rep("(raw kc143_d23125x/ and kc87_leg_lambda/$DN/)", "(raw I1101-macm3/ and kc87_leg_lambda/$DN/)", s.count("(raw kc143_d23125x/ and kc87_leg_lambda/$DN/)"))
open(X + "lane_r1.sh", "w").write(s)
# leftovers
left = [(i + 1, l[:140]) for i, l in enumerate(s.split("\n")) if "kc143_d23125x" in l or "1025" in l and "#1025" in l]
print("lines still naming kc143_d23125x or #1025:", left)
# the push script
p = open(B + "push_kc143_d23125x.sh").read()
assert p.count("I1025-macm3/kc143_d23125x") == 5 and p.count("kc143_d23125x") == 6 and p.count("push_kc143_d23125x.sh") == 1, (p.count("I1025-macm3/kc143_d23125x"), p.count("kc143_d23125x"))
open(X + "push_i1101.sh", "w").write(p.replace("I1025-macm3/kc143_d23125x", "I1101-macm3").replace("push_kc143_d23125x.sh", "push_i1101.sh"))
# blobs
def blob(f): return subprocess.check_output(["git", "hash-object", "--no-filters", X + f]).decode().strip()[:8]
ib = ["# blobs (git hash-object --no-filters, first 8) pinned by lane_r1.sh; files under in/ unless a path is given"]
for f in ("in/sol_l1kc127wind23_D23.0000.npy", "in/l1kc127wind23.jsonl", "in/kc127_syscheck_1025.py", "in/kc135_syscheck_1025.py", "in/kc143_syscheck_1025.py", "in/read_lower.py", "in/repeat_check.py", "in/d18_hybsign.py", "in/d185_scan_read.py", "in/capped_run.py", "in/launch_1070.py", "summarize_point.py", "push_i1101.sh"):
    ib.append("%s %s" % (blob(f), f))
open(X + "in_blobs.txt", "w").write("\n".join(ib) + "\n")
open(X + "scan_plan.env", "w").write('''# read by lane_r1.sh when the scan starts (appended to point.env). t5's scan (#1101 comment 7220957360): lambda 0.070, 0.085, 0.100, 0.115, 0.130 on the Rust block; the lane's repeat check (pointnew_rs.sh refuses a plan without a repeat
# on the other process) needs a repeat, here of 0.070 (round 1: both processes at 0.070). 6 evaluations on 2 processes of 4 Rust block-12 threads, 3 rounds: process 0 0.070, 0.085, 0.100; process 1 the repeat of 0.070, 0.115, 0.130.
NP=2; GATE=10; NICE=15
LAMP=("0.070" "0.070" "0.085" "0.115" "0.100" "0.130")
WIN="0.070 0.130"; REP=0.070
''')
open(X + "scan_plan_ext.env", "w").write('''# the extension scan of lane_r1.sh when the window (0.070, 0.130) reads no robust change (t5's order: "if no pair brackets in 0.070-0.130: 0.055 and 0.150 next, then report"): 0.055 and 0.150 with the window's two ends
# recomputed (0.070 and 0.130, so that a change between an old end and a new point is read in this scan alone) and a repeat of 0.055 on the other process: 5 evaluations, process 0 0.055, 0.070, 0.150; process 1 the repeat of 0.055, 0.130.
NP=2; GATE=10; NICE=15
LAMP=("0.055" "0.055" "0.070" "0.130" "0.150")
WIN="0.055 0.150"; REP=0.055
''')
d = subprocess.run(["diff", "-u", B + "lane_d23125x.sh", X + "lane_r1.sh"], capture_output=True, text=True).stdout
open(X + "diff_lane_r1.txt", "w").write(d)
print("lane_r1.sh written; diff lines:", len(d.splitlines()))
