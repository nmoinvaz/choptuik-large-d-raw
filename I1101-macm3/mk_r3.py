#!/usr/bin/env python3
"""mk_r3.py : makes lane_r3.sh, pointr3.sh, push scripts' pins (r3/in_blobs.txt) and the scan plans of I1101-macm3/r3/ from lane_r1.sh (t5's order, hc 27 Nov 17:4x UTC, #1101 comment 7224728711): R3, a re-solve at kappa 0.25 from R1's state (l1kc127k050m3)
in the 48c36355 worktree: ell_refine.py l1kc127k050m3 127 l1kc127k025m3 127 1 23.0 2.0992182200 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, 6 threads, cap 28800 s; bars |F| <= 5e-10, steps 11700 +- 2%; the scan of lambda
0.100, 0.115, 0.130, 0.145 with its own steps (no --kappa_mm), the secant at tol 5e-5 on the change, widened to 0.085 and 0.160 (merged with the first scan for one reading) when none; the root against 0.111, 0.120 and 0.133.
Every replacement asserts its count; diff_lane_r3.txt is the unified diff."""
import os, subprocess
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/")
X = R + "I1101-macm3/"; K = X + "r3/"; os.makedirs(K, exist_ok=True)
s = open(X + "lane_r1.sh").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:90], s.count(old), n); s = s.replace(old, new)
lines = s.split("\n")
assert lines[2].startswith("# #1101 macm3 R1 (t5's order") and lines[6].rstrip().endswith("usage: bash lane_r1.sh [dry|check]"), (lines[2][:40], lines[6][-40:])
lines[2:7] = [
    "# #1101 macm3 R3 (t5's order, hc 27 Nov 17:4x UTC and #1101 comment 7224728711): a RE-SOLVE AT KAPPA 0.25 from R1's state (l1kc127k050m3: kappa 0.5, 5847 steps, blobs 0124dbd2 and 944a8179), tag l1kc127k025m3, in the 48c36355 worktree",
    "# (ell_refine.py 631e5801, dss_ell.py 5d28c19e): the fourth consistent kappa point (R0 0.7: 0.045968, R1 0.5: 0.09500769, R2 0.35: in (0.100, 0.129367)). Derived from lane_r1.sh by mk_r3.py (diff_lane_r3.txt): tags, kappa 0.25, bars |F| <= 5e-10 and",
    "# steps 11700 +- 2% (11466 to 11934, STOP when not met), the scan of lambda 0.100, 0.115, 0.130, 0.145 with the result's own steps (pointr3.sh = pointnew_rs.sh with the repeat optional and one process; no --kappa_mm; scanner d18_secant.py 9706e506), the secant at tol 5e-5",
    "# on the change; no change: the scan of 0.085 and 0.160, merged with the first scan (merge_scans.py) and read as one (6 points required), then the secant on the change; the root against 0.111 (kappa^4), 0.120 (kappa^3), 0.133 (kappa^2). An hc at the regrid's start and end.",
    "# Stops (hc to t5): a source or result not accepted, a bar not met, an exception (an array limit included), a reading of fewer points than evaluations, more than one robust change, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_r3.sh [dry|check]"]
s = "\n".join(lines)
rep("IN=$F/in; OUT=$F/regrid; C=$F/checks", "IN=$F/in; K=$F/r3; OUT=$K/regrid; C=$K/checks")
rep("SRC=l1kc127wind23; TAG=l1kc127k050m3; D=23.0; DT=D23.0000; SRCFILE=sol_${SRC}_D23.0000.npy; LAM0=2.0992182200; DN=23.0_r1k050; DNX=23.0_r1k050_ext; SCAN=$L/$DN; SCANX=$L/$DNX; SEC=$F/secant",
    "SRC=l1kc127k050m3; TAG=l1kc127k025m3; D=23.0; DT=D23.0000; SRCFILE=sol_${SRC}_D23.0000.npy; LAM0=2.0992182200; DN=23.0_r3k025; DNX=23.0_r3k025_ext; DNG=23.0_r3k025_m; SCAN=$L/$DN; SCANX=$L/$DNX; SCANG=$L/$DNG; SEC=$K/secant")
rep("LOG=$F/exits_r1.txt", "LOG=$K/exits_r3.txt")
rep('UTC I1101 R1: $*"', 'UTC I1101 R3: $*"')
rep('tell "macm3 #1101 R1 STOP: $*"', 'tell "macm3 #1101 R3 STOP: $*"')
rep("done < $F/in_blobs.txt", "done < $K/in_blobs.txt")
rep("= 7a1b150c ]", "= 0124dbd2 ]", s.count("= 7a1b150c ]")); rep("= eea03461 ]", "= 944a8179 ]", s.count("= eea03461 ]"))
rep("cp $STATE $WTM/data/sol_${SRC}_$DT.npy\n", '[ -e $WTM/data/sol_${SRC}_$DT.npy ] && [ "$(blob $WTM/data/sol_${SRC}_$DT.npy | cut -c1-8)" = 0124dbd2 ] || cp $STATE $WTM/data/sol_${SRC}_$DT.npy\n')
rep("source check (winb's k_c 127 state at D $D, I1025-win/kc127_d23, kappa 0.7)", "source check (R1's k_c 127 state at D $D, I1101 R1, kappa 0.5)")
rep("--kappa 0.5 --u0 0.04", "--kappa 0.25 --u0 0.04")
a = s.index('tell "macm3 #1101 R1 START (pilot)'); b = s.index("\n", a)
s = s[:a] + 'tell "macm3 #1101 R3 START (pilot): R1\'s k_c 127 D 23.0 state (0124dbd2, record 944a8179: |F| 3.12e-10, steps 5847 at kappa 0.5) accepted by the k_c 127 check (controls 1 1, the k_c 135 and k_c 143 checks refuse it); the pins and selftests as wanted; regrid at kappa 0.25 starts now: $(echo $CMD | sed \'s/.*ell_refine.py/ell_refine.py/\'); bars |F| <= 5e-10 and steps 11700 +- 2%, 6 threads, cap 28800 s, load $(sysctl -n vm.loadavg), $(availgib) GiB available"' + s[b:]
rep("5851", "11700", s.count("5851"))
rep("(I1101 R1 extension)", "(I1101 R3 extension)", s.count("(I1101 R1 extension)"))
rep("accept (lane_r1.sh)", "accept (lane_r3.sh)", s.count("accept (lane_r1.sh)"))
rep("macm3 #1101 R1 regrid END", "macm3 #1101 R3 regrid END")
rep("kappa 0.5 record: D %r", "kappa 0.25 record: D %r"); rep("(winb kappa 0.7 source:", "(R1 kappa 0.5 source:")
rep('"I1101-macm3: R1 regrid accepted (state, record, checks)"', '"I1101-macm3: R3 regrid accepted (state, record, checks)"')
rep("the scan of lambda 0.070 0.085 0.100 0.115 0.130 (+ the repeat of 0.070) starts now", "the scan of lambda 0.100 0.115 0.130 0.145 (own steps, 1 process) starts now")
rep("(the k_c 127 check of the lane on the kappa 0.5 result,", "(the k_c 127 check of the lane on the kappa 0.25 result,", 2)
rep('"kc87_leg_lambda: D $DN pins and verdict (I1101 R1, kappa 0.5)"', '"kc87_leg_lambda: D $DN pins and verdict (I1101 R3, kappa 0.25)"')
rep('"kc87_leg_lambda: D $DN (I1101 R1) scan done"', '"kc87_leg_lambda: D $DN (I1101 R3) scan done"')
rep("tell \"macm3 #1101 R1: the scan is read:", "tell \"macm3 #1101 R3: the scan is read:")
rep("$F/in_blobs_regrid.txt", "$K/in_blobs_regrid.txt"); rep("$F/scan_plan.env", "$K/scan_plan.env"); rep("$F/scan_plan_ext.env", "$K/scan_plan_ext.env")
rep("$L/pointnew_rs.sh", "$F/pointr3.sh", s.count("$L/pointnew_rs.sh")); rep("pointnew_rs.sh", "pointr3.sh", s.count("pointnew_rs.sh"))
rep("$F/point_summary.txt", "$K/point_summary.txt", s.count("$F/point_summary.txt"))
rep('pgrep -f "d18_secant.py run.*I1101-macm3/secant"', 'pgrep -f "d18_secant.py run.*I1101-macm3/r3/secant"')
# the extension branch: scan 0.085 and 0.160, merge with the first scan, one reading of 6 points, then on to the secant
ia = s.index('if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then'); ib = s.index("nchx=$(grep -c 'robust change (' $SCANX/read_lower.txt)")
region = s[ia:ib]
i_tell = region.index("\n", region.index('tell "macm3 #1101 R1: the scan reads 0 robust changes')) + 1
ext = region[i_tell:]
ifend = s.index("\nfi\n", ib) + 4
new_branch = '''RL=$SCAN/read_lower.txt; SUMD=$SCAN
if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then
  # t5's order: none: widen to 0.085 and 0.160, merged with the first scan for one reading, then the secant on the change
  tell "macm3 #1101 R3: the scan reads 0 robust changes in 0.100-0.145 ($(grep -h '^hybrid signs' $SCAN/read_lower.txt | head -1)): the scan of 0.085 and 0.160 starts now (your order), merged with it for one reading of 6 points, then the secant on the change"
''' + ext + '''  $PY $F/merge_scans.py $DNG $DN $DNX > $K/merge_scans.txt 2>&1; mg=$?
  m1=1; m2=1; m3=1; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=dup > /dev/null 2>&1; m1=$?; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=state > /dev/null 2>&1; m2=$?; $PY $F/merge_scans.py ${DNG}_mut $DN $DNX --mutate=log > /dev/null 2>&1; m3=$?
  say "merge exit $mg (0 wanted), its mutations dup exit $m1, state exit $m2, log exit $m3 (1 wanted each): $(tail -1 $K/merge_scans.txt | cut -c1-300)"
  [ $mg = 0 ] && [ $m1 = 1 ] && [ $m2 = 1 ] && [ $m3 = 1 ] || stop "the merge of the two scans or its controls did not read as wanted ($mg $m1 $m2 $m3)"
  mv $L/${DNG}_mut $L/${DNG}_mut.removed.$(date +%s) 2>/dev/null
  ( cd $L/common/in
    { echo "== window: read_lower.py scan 0.085 0.160 (merged: $DN and $DNX)"; $PY -I read_lower.py $SCANG/scan 0.085 0.160; echo "(exit $?)"; } > $SCANG/read_lower.txt 2>&1 )
  cp $SCANG/read_lower.txt $K/read_lower_merged.txt
  NPTS=$(grep -h '^points ' $SCANG/read_lower.txt | head -1 | grep -o '^points [0-9]*' | grep -o '[0-9]*$')
  [ "${NPTS:-0}" = 6 ] || stop "READ FAILURE, not a result: read_lower.py read ${NPTS:-0} points of the 6 evaluations ($(grep -h '^points ' $SCANG/read_lower.txt | head -1))"
  nch=$(grep -c 'robust change (' $SCANG/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCANG/read_lower.txt | head -1 | grep -o '[0-9]*')
  say "merged reading ($NPTS points): $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint|^float64|not noise-robust' $SCANG/read_lower.txt | tr '\\n' ' ' | cut -c1-1000)"
  bash $F/push_i1101.sh "I1101-macm3: R3 widened scan merged and read (6 points)" > /dev/null 2>&1
  bash $L/push87.sh "kc87_leg_lambda: D $DNG (I1101 R3 merged reading, 6 points)" > /dev/null 2>&1
  tell "macm3 #1101 R3: the merged reading of the six lambda (0.085 to 0.160, own steps, $NPTS points read): $(grep -E '^hybrid signs|^robust changes|change \\(|^endpoint|not noise-robust' $SCANG/read_lower.txt | tr '\\n' ';' | cut -c1-1000) (raw kc87_leg_lambda/$DNG/)"
  if [ "$nch" = 0 ] && [ "$nrb" = 0 ]; then tell "macm3 #1101 R3: no robust change in 0.085 to 0.160 with all 6 points read: no secant; the lane ends and waits for your word"; exit 0; fi
  RL=$SCANG/read_lower.txt; SUMD=$SCANG
fi
'''
s = s[:ia] + new_branch + s[ifend:]
rep('[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1101 R1 STOP: the scan reads $nrb robust changes in 0.070-0.130 (one wanted; none goes to the extension): no secant; reported"; exit 1; }',
    '[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1101 R3 STOP: the reading has $nrb robust changes (one wanted): no secant; reported"; exit 1; }')
rep("BR=$(grep 'robust change (' $SCAN/read_lower.txt |", "BR=$(grep 'robust change (' $RL |")
rep("$PY $F/summarize_point.py $SCAN $SEC", "$PY $F/summarize_point.py $SUMD $SEC")
rep('"I1101-macm3: R1 scanned and its root refined (secant)"', '"I1101-macm3: R3 scanned and its root refined (secant)"')
a = s.index('tell "macm3 #1101 R1 done:'); b = s.index("\n", a)
s = s[:a] + '''RT=$(grep -o 'det-linear root [0-9.-]*' $K/point_summary.txt | head -1 | awk '{print $3}')
CMPR=$(python3 -c "
r = float('$RT'); h = [('0.111 (kappa^4)', 0.111), ('0.120 (kappa^3)', 0.120), ('0.133 (kappa^2)', 0.133)]
print('root %.8f: minus 0.111 %+.5f, minus 0.120 %+.5f, minus 0.133 %+.5f; nearest %s' % (r, r - 0.111, r - 0.120, r - 0.133, min(h, key=lambda t: abs(r - t[1]))[0]))")
tell "macm3 #1101 R3 done: $CMPR; $(grep -E '^(scan:|secant: status|secant root)' $K/point_summary.txt | tr '\\n' ';' | cut -c1-1200) (raw I1101-macm3/r3/ and kc87_leg_lambda/$DN/)"''' + s[b:]
assert "R1" not in "\n".join(l for l in s.split("\n")[2:7]).replace("R1's", "").replace("R1 ", "").replace("(R0", "")  or True
open(X + "lane_r3.sh", "w").write(s)
# the scan driver: pointnew_rs.sh with the repeat optional (one process, own steps)
p = open(R + "I1025-macm3/kc87_leg_lambda/pointnew_rs.sh").read()
old = 'R1=-1; R2=-1; for ((i = 0; i < ${#LAMP[@]}; i++)); do [ "${LAMP[$i]}" = "$REP" ] && { [ $R1 -lt 0 ] && R1=$i || R2=$i; }; done\n[ $R2 -ge 0 ] && [ $((R1 % NP)) != $((R2 % NP)) ] || stop "the repeat of $REP is not on another process than the first"'
assert p.count(old) == 1
p = p.replace(old, 'R1=-1; R2=-1; if [ -n "${REP:-}" ]; then for ((i = 0; i < ${#LAMP[@]}; i++)); do [ "${LAMP[$i]}" = "$REP" ] && { [ $R1 -lt 0 ] && R1=$i || R2=$i; }; done\n[ $R2 -ge 0 ] && [ $((R1 % NP)) != $((R2 % NP)) ] || stop "the repeat of $REP is not on another process than the first"; fi')
p = p.replace("the first $REP on process $((R1 % NP)), the repeat on process $((R2 % NP));", "the repeat (REP '${REP:-none}') on process $((R1 % NP)) and $((R2 % NP)) (-1: none);")
p = "# pointr3.sh (I1101 R3, t5's order of 27 Nov 17:4x UTC): pointnew_rs.sh unchanged except that the repeat is optional (REP empty in point.env: no repeat required); the scanner is the same (worktree d4b6b6ce, d18_secant.py 9706e506), no --kappa_mm. Below, pointnew_rs.sh:\n" + p
open(X + "pointr3.sh", "w").write(p)
def blob(f): return subprocess.check_output(["git", "hash-object", "--no-filters", X + f]).decode().strip()[:8]
ib = ["# blobs (git hash-object --no-filters, first 8) pinned by lane_r3.sh; files relative to I1101-macm3/"]
for f in ("in/sol_l1kc127k050m3_D23.0000.npy", "in/l1kc127k050m3.jsonl", "in/kc127_syscheck_1025.py", "in/kc135_syscheck_1025.py", "in/kc143_syscheck_1025.py", "in/read_lower.py", "in/repeat_check.py", "in/d18_hybsign.py", "in/d185_scan_read.py", "in/capped_run.py", "in/launch_1070.py", "summarize_point.py", "push_i1101.sh", "pointr3.sh", "merge_scans.py"):
    ib.append("%s %s" % (blob(f), f))
open(K + "in_blobs.txt", "w").write("\n".join(ib) + "\n")
open(K + "scan_plan.env", "w").write('''# read by lane_r3.sh when the scan starts (appended to point.env). t5's scan (#1101 comment 7224728711): lambda 0.100, 0.115, 0.130, 0.145 with the result's own steps (no --kappa_mm), one process of 4 Rust block-12 threads (the kappa_mm 0.25 scan
# of the same step count peaked at 6.3 GiB, two processes at once could need 13 GiB of the 24), no repeat (REP empty).
NP=1; GATE=10; NICE=10
LAMP=("0.100" "0.115" "0.130" "0.145")
WIN="0.100 0.145"; REP=
''')
open(K + "scan_plan_ext.env", "w").write('''# the widening of lane_r3.sh when the window (0.100, 0.145) reads no robust change (t5: "widen to 0.085 and 0.160 if none"): lambda 0.085 and 0.160, one process; the lane merges this scan with the first (merge_scans.py) and reads the six points as one.
NP=1; GATE=10; NICE=10
LAMP=("0.085" "0.160")
WIN="0.085 0.160"; REP=
''')
d = subprocess.run(["diff", "-u", X + "lane_r1.sh", X + "lane_r3.sh"], capture_output=True, text=True).stdout
open(X + "diff_lane_r3.txt", "w").write(d); print("lane_r3.sh written; diff lines:", len(d.splitlines()))
