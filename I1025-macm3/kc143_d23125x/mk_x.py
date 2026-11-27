#!/usr/bin/env python3
"""mk_x.py : makes lane_d23125x.sh, push_kc143_d23125x.sh, in_blobs.txt and scan_plan.env of kc143_d23125x/ from the files of kc143_d23125/ (t5's order, #1025 comment 7213649039:
regrid k_c 143 at D 23.125 directly from the k_c 127 state there, skipping k_c 135; the regrid line with only the source tag and its k_c changed; scan lambda -0.030, -0.025, -0.020 and the secant at tol 5e-5 on the Rust block).
Every replacement asserts its count; the unified diff of the lane goes to diff_lane_x.txt. Run from anywhere; writes into kc143_d23125x/."""
import os, re, subprocess, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
B = R + "kc143_d23125/"; X = R + "kc143_d23125x/"
s = open(B + "lane_d23125.sh").read()


def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old, s.count(old), n)
    s = s.replace(old, new)


rep("kc143_d23125", "kc143_d23125x", s.count("kc143_d23125"))   # folder, labels, the push script, the secant's pgrep pattern (before the new header is inserted)
# header: lines 3-8 (the derivation, the steps; indices 2 to 7) replaced by five lines
lines = s.split("\n"); assert lines[2].startswith("# #1025 macm3 kc143_d23125x (t5's order") and lines[7].rstrip().endswith("usage: bash lane_d23125.sh [dry|check]"), (lines[2][:60], lines[7][-60:])
hdr = [
    "# #1025 macm3 kc143_d23125x (t5's order, hc 27 Nov 08:3x UTC and #1025 comment 7213649039): the k_c 143 state at D 23.125 REGRIDDED DIRECTLY from my k_c 127 state there (kc127_leg, tag l1kc127Lmacm3; state blob e1dccb3c, record 58d3b080, copies in in/),",
    "# skipping k_c 135: a cross-path check of kc143_d23125 (lambda_1 -0.02449537 there). Derived from kc143_d23125/lane_d23125.sh by mk_x.py (diff_lane_x.txt): the source tag l1kc127Lmacm3 and its k_c 127 in the regrid line, the destination tag l1kc143macm3d23125x (the earlier",
    "# k_c 143 record keeps its name), the source check (the k_c 127 check accepts the state, controls exit 1 1, the k_c 135 and k_c 143 checks refuse it), the pinned inputs and the folder names. Everything else as in that lane: kappa 0.7, u0 0.04, Ks 30, tol 1e-12, --no-gamma, 6 threads, nice 10, cap 28800 s,",
    "# the k_c 143 check on the result, the scanner d18_secant.py 9706e506 (Rust block 12, 4 threads, 2 processes), the one-change rule, the secant (tol 5e-5, maxev 10, one process). The scan: lambda -0.030, -0.025, -0.020 plus the repeat of -0.030 that the lane's repeat check needs (scan_plan.env).",
    "# Stops (hc to t5): a source or result not accepted (the regrid included), an exception (an array limit included), no robust change or more than one, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_d23125x.sh [dry|check]",
    ]
lines[2:8] = hdr[:5]
s = "\n".join(lines)
rep("SRC=l1kc135macm3d23125; TAG=l1kc143macm3d23125;", "SRC=l1kc127Lmacm3; TAG=l1kc143macm3d23125x;")
rep("DN=23.125_kc143;", "DN=23.125_kc143x;")
rep("= ac01e477 ]", "= e1dccb3c ]")
rep("ell_refine.py $SRC 135 $TAG 143 1", "ell_refine.py $SRC 127 $TAG 143 1")
# the source check block
old_start = s.index("# 3. the source:"); old_end = s.index("[ \"$MODE\" = dry ]")
new_block = '''# 3. the source: the k_c 127 check accepts it with controls 1 1; the k_c 135 and k_c 143 checks refuse it
STATE=$IN/$SRCFILE; REC=$IN/$SRC.jsonl
C127S="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $REC $STATE $D $WTM"
$C127S > $OUT/source_syscheck.txt 2>&1; s0=$?; $C127S --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?; $C127S --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc135_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc135check_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/kc143_syscheck_1025.py $REC $STATE $D $WTM > $OUT/source_kc143check_refuses.txt 2>&1; s4=$?
say "source check (my k_c 127 state at D $D, kc127_leg): kc127_syscheck exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc135_syscheck on the source exit $s3, kc143_syscheck on the source exit $s4 (1 wanted each): $(grep -E '^D ' $OUT/source_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
'''
s = s[:old_start] + new_block + s[old_end:]
rep("(k_c 135 source: |F|", "(k_c 127 source: |F|")
rep('src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]', 'src = [json.loads(l) for l in open(sys.argv[2]) if l.strip() and json.loads(l)["D"] == float(sys.argv[3])][-1]')
open(X + "lane_d23125x.sh", "w").write(s)
# the push script
p = open(B + "push_kc143_d23125.sh").read(); assert p.count("kc143_d23125") == 6, p.count("kc143_d23125")
open(X + "push_kc143_d23125x.sh", "w").write(p.replace("kc143_d23125", "kc143_d23125x"))
# blobs
def blob(f): return subprocess.check_output(["git", "hash-object", "--no-filters", X + f]).decode().strip()[:8]
ib = ["# blobs (git hash-object --no-filters, first 8) pinned by lane_d23125x.sh; files under in/ unless a path is given"]
for f in ("in/sol_l1kc127Lmacm3_D23.1250.npy", "in/l1kc127Lmacm3.jsonl", "in/kc127_syscheck_1025.py", "in/kc135_syscheck_1025.py", "in/kc143_syscheck_1025.py", "in/read_lower.py", "in/repeat_check.py", "in/d18_hybsign.py", "in/d185_scan_read.py", "in/capped_run.py", "in/launch_1070.py", "summarize_point.py", "push_kc143_d23125x.sh"):
    ib.append("%s %s" % (blob(f), f))
open(X + "in_blobs.txt", "w").write("\n".join(ib) + "\n")
open(X + "scan_plan.env", "w").write('''# read by lane_d23125x.sh when the scan starts (appended to point.env). t5's scan (#1025 comment 7213649039): lambda -0.030, -0.025, -0.020; the lane's repeat check (pointnew_rs.sh refuses a plan without a repeat on the other process)
# needs the repeat of -0.030, so 4 evaluations on 2 processes of 4 Rust block-12 threads, 2 rounds: process 0 -0.030, -0.025; process 1 the repeat of -0.030, -0.020. The window of the read is (-0.030, -0.020): a root below -0.030 reads as no robust change.
NP=2; GATE=10; NICE=15
LAMP=("-0.030" "-0.030" "-0.025" "-0.020")
WIN="-0.030 -0.020"; REP=-0.030
''')
d = subprocess.run(["diff", "-u", B + "lane_d23125.sh", X + "lane_d23125x.sh"], capture_output=True, text=True).stdout
open(X + "diff_lane_x.txt", "w").write(d)
print("lane_d23125x.sh written; diff lines:", len(d.splitlines()))
