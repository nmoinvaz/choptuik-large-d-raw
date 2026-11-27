#!/usr/bin/env python3
"""mk_kmm3.py : makes lane_kmm3.sh of I1101-macm3/ from lane_kmm2.sh: the K4w scan (lambda 0.070 0.085 0.160 0.180) stands, so the lane starts at the merge, which now also writes the file name read_lower.py reads (scan_*_p*.jsonl;
the first reading of K4w said 'points 0' for that reason, t5's hc 17:4x UTC), refuses a reading whose point count is not 8 (a read failure, not a result), and runs the secant at tol 5e-5 with --kappa_mm=0.25 on the first robust change.
Every replacement asserts its count; diff_lane_kmm3.txt is the unified diff."""
import os, subprocess
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1101-macm3/")
s = open(R + "lane_kmm2.sh").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:80], s.count(old), n); s = s.replace(old, new)
lines = s.split("\n")
assert lines[1].startswith("# #1101 macm3 K4w (t5's order") and lines[4].startswith("# Stops (hc to t5)"), (lines[1][:30], lines[4][:30])
lines[1:5] = [
    "# #1101 macm3 K4w2 (t5's hc 27 Nov 17:4x UTC: 'points 0' is a read failure, not a result): the K4w scan (kappa_mm 0.25, lambda 0.070 0.085 0.160 0.180, kc87_leg_lambda/23.0_r1k050_kmm025w) and the K4 scan (0.100 to 0.145) stand; this lane merges them again",
    "# (merge_kmm.py now also writes scan_D23.0_p0.jsonl, the name read_lower.py reads), reads the window (0.070, 0.180), REFUSES a reading whose point count is not 8, reports the eight signs, and runs the secant at tol 5e-5 with --kappa_mm=0.25 on the first",
    "# (lowest-lambda) robust change; a second one is named in the hc, not run. Derived from lane_kmm2.sh by mk_kmm3.py (diff_lane_kmm3.txt).",
    "# Stops (hc to t5): a pin or selftest that does not read as wanted, the merge refused, a reading of fewer than 8 points, an exception, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_kmm3.sh [dry]"]
s = "\n".join(lines)
rep("LOG=$K/exits_kmm_w.txt", "LOG=$K/exits_kmm_w2.txt")
rep('say() { echo "== $(stamp) UTC I1101 K4w: $*"', 'say() { echo "== $(stamp) UTC I1101 K4w2: $*"')
rep('tell "macm3 #1101 K4w STOP: $*"', 'tell "macm3 #1101 K4w2 STOP: $*"')
i4 = s.index("# 4. the scan of the same state at kappa_mm 0.25, lambda 0.070 0.085 0.160 0.180"); im = s.index("# the merged scan of the eight lambda and its reading")
s = s[:i4] + '''# 4. the two scans stand (K4: 0.100 to 0.145; K4w: 0.070 0.085 0.160 0.180)
[ -e $L/$DNM/SCAN_DONE.txt ] && [ -e $SCANW/SCAN_DONE.txt ] && [ -s $K/control_compare.txt ] || stop "a scan or the control comparison is missing"
say "the scans stand: $DNM (0.100 to 0.145) and $DNW (0.070 0.085 0.160 0.180), both at --kappa_mm=0.25; the control of K4 (kappa_mm 0.5, bit for bit, kmm025/control_compare.txt) stands; the first reading of the merge said 'points 0' (read_lower.py reads scan_*_p*.jsonl; merge_kmm.py now writes that name too)"
''' + s[im:]
rep("mv $L/${DNG}_mut $L/${DNG}_mut.removed.$(date +%s) 2>/dev/null\n", "mv $L/${DNG}_mut $L/${DNG}_mut.removed.$(date +%s) 2>/dev/null\n[ -e $SCANG/read_lower.txt ] && mv $SCANG/read_lower.txt $SCANG/read_lower.txt.superseded.$(date +%s)\n")
rep("cp $SCANG/read_lower.txt $K/read_lower_merged.txt\n", "cp $SCANG/read_lower.txt $K/read_lower_merged.txt\nNPTS=$(grep -h '^points ' $SCANG/read_lower.txt | head -1 | grep -o '^points [0-9]*' | grep -o '[0-9]*$')\n[ \"${NPTS:-0}\" = 8 ] || stop \"READ FAILURE, not a result: read_lower.py read ${NPTS:-0} points of the 8 evaluations ($(grep -h '^points ' $SCANG/read_lower.txt | head -1))\"\n")
rep('tell "macm3 #1101 K4w: the eight signs at --kappa_mm=0.25 (merged scan, lambda 0.070 to 0.180): ', 'tell "macm3 #1101 K4w2: the eight signs at --kappa_mm=0.25 (merged scan, lambda 0.070 to 0.180, $NPTS points read): ')
rep('tell "macm3 #1101 K4w: no robust change in 0.070 to 0.180 at --kappa_mm=0.25 ($SIGNS)', 'tell "macm3 #1101 K4w2: no robust change in 0.070 to 0.180 at --kappa_mm=0.25 with all 8 points read ($SIGNS)')
rep('tell "macm3 #1101 K4w: $nch robust changes', 'tell "macm3 #1101 K4w2: $nch robust changes')
rep('tell "macm3 #1101 K4w done', 'tell "macm3 #1101 K4w2 done')
rep('bash $F/push_i1101.sh "I1101-macm3: K4w scan (0.070 0.085 0.160 0.180) read, merged with K4\'s"', 'bash $F/push_i1101.sh "I1101-macm3: K4w2 merged reading of the eight lambda (8 points)"')
rep('bash $L/push87.sh "kc87_leg_lambda: D $DNG (I1101 K4w merged reading)"', 'bash $L/push87.sh "kc87_leg_lambda: D $DNG (I1101 K4w2 merged reading, 8 points)"')
rep("$K/point_summary_w.txt", "$K/point_summary_w2.txt", s.count("$K/point_summary_w.txt"))
rep("(raw I1101-macm3/kmm025/ and kc87_leg_lambda/$DNW/)", "(raw I1101-macm3/kmm025/ and kc87_leg_lambda/$DNG/)")
open(R + "lane_kmm3.sh", "w").write(s)
d = subprocess.run(["diff", "-u", R + "lane_kmm2.sh", R + "lane_kmm3.sh"], capture_output=True, text=True).stdout
open(R + "diff_lane_kmm3.txt", "w").write(d); print("lane_kmm3.sh written; diff lines:", len(d.splitlines()))
