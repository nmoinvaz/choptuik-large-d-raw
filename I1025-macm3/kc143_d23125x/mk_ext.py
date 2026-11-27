#!/usr/bin/env python3
"""mk_ext.py : makes ext_d23125x.sh of kc143_d23125x/ from the stages 6 and 7 (scan folder, scan, one-change rule, secant, summary) of lane_d23125x.sh, with the replacements asserted; diff_ext.txt lists them.
ext_d23125x.sh waits for the lane's "the scan reads 0 robust changes" report, picks the side with ext_side.py (t5's pre-authorization, #1025 hc 27 Nov 08:4x UTC), builds the folder kc87_leg_lambda/23.125_kc143x_ext
from the lane's pinned state and record (same raw commit), runs the extension scan (scan_plan_ext_<side>.env) and, on exactly one robust change, the secant at tol 5e-5. Test knobs (env, for the sandbox test only): TESTMODE=dry
(no wait, no scan: the side, the folder, the pins and pointnew_rs.sh dry), FX (the lane folder), LOGX (the log), MAIN (the main scan folder name), TAGX, DNE (the extension folder name), READ (the read_lower.txt to decide on)."""
import os, re, subprocess
X = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125x/")
lane = open(X + "lane_d23125x.sh").read()
i6 = lane.index("# 6. the scan folder"); end = lane.rindex("exit 0\n}")
body = lane[i6:end]


def rep(old, new, n=1):
    global body
    assert body.count(old) == n, (old, body.count(old), n)
    body = body.replace(old, new)


rep('RAWC=$(echo "$RP" | awk \'{print $2}\')', 'RAWC=$(grep \'^RAWC=\' $L/$MAIN/point.env | cut -d= -f2); [ -n "$RAWC" ] || stop "no RAWC in $L/$MAIN/point.env"')
rep("cat $F/scan_plan.env; } > $SCAN/point.env", "cat $KX/scan_plan_ext_$SIDE.env; } > $SCAN/point.env")
rep("SRC=I1025-macm3/kc143_d23125x/in", "SRC=I1025-macm3/$(basename $F)/in")
rep("$RAWC:I1025-macm3/kc143_d23125x/in/$TAG.jsonl", "$RAWC:I1025-macm3/$(basename $F)/in/$TAG.jsonl")
# the lines that use the regrid's check variables c0 c1 c2 c3: the verdict is the lane's own
rep('echo "ACCEPTED $(stamp) UTC (the k_c 143 regrid check of the lane, $OUT/syscheck.txt; controls and the k_c 135 refusal in $OUT)" > $SCAN/VERDICT.txt',
    'echo "ACCEPTED $(stamp) UTC (inherited from the lane: $(cat $OUT/VERDICT.txt); the k_c 143 regrid check of the lane, $OUT/syscheck.txt)" > $SCAN/VERDICT.txt')
i = body.index('echo "$(stamp) UTC accept (lane_d23125.sh)'); j = body.index("\n", i)
body = body[:i] + 'echo "$(stamp) UTC accept (ext_d23125x.sh): the lane\'s regrid verdict, $(cat $OUT/VERDICT.txt); the extension scan (side $SIDE) of the main scan $MAIN: $(grep -E \'^D \' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt' + body[j:]
rep('"kc87_leg_lambda: D $DN pins and verdict (kc143 regrid of D 23.125)"', '"kc87_leg_lambda: D $DN pins and verdict (extension scan, side $SIDE)"')
rep('"kc87_leg_lambda: D $DN (k_c 143) scan done"', '"kc87_leg_lambda: D $DN (k_c 143, extension scan) scan done"')
rep("the scan reads $nrb robust changes (one wanted): no secant refinement; reported, the window is not widened without your word\"; exit 0; }",
    "the EXTENSION scan (side $SIDE) reads $nrb robust changes (one wanted): no secant refinement; stopped, your word\"; exit 0; }")
rep("the k_c 143 D 23.125 scan is read:", "the k_c 143 D 23.125 EXTENSION scan (side $SIDE) is read:")
rep("tell \"macm3 #1025 kc143_d23125x done: ", "tell \"macm3 #1025 kc143_d23125x done: [extension scan, side $SIDE; the window of the lane read no robust change] ")
pre = r'''#!/bin/bash
# #1025 macm3 kc143_d23125x, the extension scan (t5's pre-authorization, hc 27 Nov 08:4x UTC, in README.md): made by mk_ext.py from the stages 6 and 7 of lane_d23125x.sh (diff_ext.txt); started with the lane and polling.
# It acts only when the lane's exits file says "the scan reads 0 robust changes" (the window (-0.030, -0.020) had no robust change) and ext_side.py reads '-' at every point (extend to -0.035 and -0.040) or '+' at every point (-0.015 and -0.010);
# any other reading or a non-robust point: it tells t5 and stops. The extension scan runs in kc87_leg_lambda/23.125_kc143x_ext on the same pinned state and record, recomputing the window's three points (scan_plan_ext_<side>.env),
# then the secant at tol 5e-5 on the one robust change. Test knobs for the sandbox test only: TESTMODE=dry NOWAIT LANEPAT FX LOGX MAIN TAGX DNE READ.
{
set -u
TESTMODE=${TESTMODE:-}
KX=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125x
F=${FX:-$KX}; IN=$F/in; OUT=$F/regrid; C=$F/checks
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
WTS=$HOME/Source/choptuik-large-d-1102m3/solver/matter; SITE=$HOME/Source/ellrs-site-1102m3
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
TAG=${TAGX:-l1kc143macm3d23125x}; D=23.125; DT=D23.1250; MAIN=${MAIN:-23.125_kc143x}; DN=${DNE:-23.125_kc143x_ext}; SCAN=$L/$DN; SEC=$F/secant
HC=$(command -v hc); LOG=${LOGX:-$F/exits_kc143.txt}
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc143_d23125x ext: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && [ -z "$TESTMODE" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { tell "macm3 #1025 kc143_d23125x ext STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
export PYTHONDONTWRITEBYTECODE=1
say "extension watcher started (pid $$; mode ${TESTMODE:-full}); waiting for the lane's scan report"
LANEPAT=${LANEPAT:-kc143_d23125x/lane_d23125x.sh}
if [ -z "${NOWAIT:-}" ]; then
  while :; do
    grep -q 'the scan reads 0 robust changes' $LOG && break
    if ! pgrep -f "$LANEPAT" > /dev/null; then
      sleep 5; grep -q 'the scan reads 0 robust changes' $LOG && break
      say "the lane ended without a scan that read no robust change: nothing to extend"; exit 0
    fi
    sleep 30
  done
  while pgrep -f "$LANEPAT" > /dev/null; do sleep 5; done
fi
READ=${READ:-$L/$MAIN/read_lower.txt}
SIDE=$($PY $KX/ext_side.py $READ); [ "$SIDE" = low ] || [ "$SIDE" = high ] || stop "the window reads no robust change but not the same sign at every point (or a non-robust point): ext_side.py says '$SIDE'; not covered by t5's order, your word"
say "the window read no robust change, side $SIDE: the extension scan (scan_plan_ext_$SIDE.env) on the same state"
[ -e $SCAN/SCAN_DONE.txt ] && stop "$SCAN/SCAN_DONE.txt exists"
'''
post = r'''
exit 0
}
'''
# in test mode (dry) the stage ends after the pins and pointnew_rs.sh dry
body = body.replace("echo \"$(stamp) UTC accept (ext_d23125x.sh)", "echo \"$(stamp) UTC accept (ext_d23125x.sh)", 1)
marker = "bash $L/push87.sh \"kc87_leg_lambda: D $DN pins and verdict (extension scan, side $SIDE)\" > /dev/null 2>&1"
assert body.count(marker) == 1
body = body.replace(marker, "[ \"$TESTMODE\" = dry ] && { bash $L/pointnew_rs.sh $DN dry > $SCAN/dry.txt 2>&1; say \"dry: pointnew_rs.sh dry exit $? ($(tail -1 $SCAN/dry.txt))\"; exit 0; }\n" + marker)
out = pre + body + post.lstrip("\n")
open(X + "ext_d23125x.sh", "w").write(out)
print("ext_d23125x.sh written,", len(out.splitlines()), "lines")
