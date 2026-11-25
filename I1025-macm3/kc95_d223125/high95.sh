#!/bin/bash
# #1025 macm3 kc95_d223125: the HIGH scan of the k_c 95 D 22.3125 state (t5, hc 25 Nov ~11:0x UTC: "the k_c 95 D 22.3125 high scan (0.50 to 0.70 by 0.02 plus a repeat), registered as before").
# Same pinned state and record as the wide scan (folder 22.3125_kc95; raw 33f6e5929), folder 22.3125_kc95_high, lambda 0.50 to 0.70 by 0.02 + a repeat of 0.60, 4 processes of 1 thread at nice 15 (point87.sh scan),
# read by read_lower.py and wide_read.py. Pins, selftests and their mutations are lane95.sh's (lines 27 and 41 to 56, copied below unchanged except the checks folder). Predictions are registered in README.md before this runs.
# Stops (hc to t5): a pin, selftest or mutation that does not read as written, a scan failure. usage: bash high95.sh
{
set -u
F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc95_d223125; IN=$F/in; C=$F/checks_high
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
TAG=l1kc95macm3d223125; D=22.3125; DN=22.3125_kc95_high; SCAN=$L/$DN
HC=$(command -v hc); LOG=$F/exits_kc95.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc95_d223125 high scan: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { mkdir -p $SCAN; echo "REFUSED: $*" > $SCAN/VERDICT.txt; tell "macm3 #1025 kc95_d223125 high scan STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $C
export PYTHONDONTWRITEBYTECODE=1
say "start (load $(sysctl -n vm.loadavg))"
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f | cut -c1-8)" = "$bb" ] || stop "$IN/$f missing or not blob $bb"; done < $F/in_blobs.txt
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
# 2. selftests
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( cd $IN
  nice -n 10 $PY -I kc87_syscheck_1025.py --selftest > $C/selftest_kc87_syscheck.txt 2>&1; a0=$?
  nice -n 10 $PY -I kc95_syscheck_1025.py --selftest > $C/selftest_kc95_syscheck.txt 2>&1; a1=$?
  $PY -W ignore read_lower.py selftest > $C/selftest_read_lower.txt 2>&1; r0=$?
  $PY -W ignore read_lower.py selftest --mutate=shift > $C/selftest_read_lower_shift.txt 2>&1; r1=$?
  $PY -W ignore read_lower.py selftest --mutate=round2 > $C/selftest_read_lower_round2.txt 2>&1; r2=$?
  $PY repeat_check.py selftest > $C/selftest_repeat_check.txt 2>&1; r3=$?
  $PY -I wide_read.py selftest > $C/selftest_wide_read.txt 2>&1; w0=$?
  $PY -I wide_read.py selftest --mutate > $C/selftest_wide_read_mutate.txt 2>&1; w1=$?
  ( cd $F && $PY -I in/planted_wide.py in > $C/selftest_planted_wide.txt 2>&1 ); p0=$?
  ( cd $F && $PY -I in/planted_wide.py --mutate in > $C/selftest_planted_wide_mutate.txt 2>&1 ); p1=$?
  echo "$a0 $a1 $r0 $r1 $r2 $r3 $w0 $w1 $p0 $p1" > $C/selftest_exits.txt )
[ "$(cat $C/selftest_exits.txt)" = "0 0 0 1 1 0 0 1 0 1" ] || stop "the selftests did not behave ($(cat $C/selftest_exits.txt); wanted 0 0 0 1 1 0 0 1 0 1: kc87_syscheck, kc95_syscheck, read_lower, mutate shift, mutate round2, repeat_check, wide_read, mutate, planted_wide, mutate)"
say "selftests as wanted (0 0 0 1 1 0 0 1 0 1)"
RAWC=$(grep '^RAWC=' $L/22.3125_kc95/point.env | cut -d= -f2); [ "$RAWC" = 33f6e5929 ] || stop "RAWC of the wide scan is $RAWC, not 33f6e5929"
git -C $RAWG cat-file -e $RAWC:I1025-macm3/kc95_d223125/in/$TAG.jsonl 2>/dev/null || stop "the commit $RAWC does not hold the regrid record"
[ ! -e $SCAN/SCAN_DONE.txt ] || stop "$SCAN already has SCAN_DONE.txt"
mkdir -p $SCAN
cat > $SCAN/point.env <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_D22.3125.npy
STATEBLOB=$(blob $IN/sol_${TAG}_D22.3125.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
# t5's order (hc 25 Nov): the high scan of macm3's k_c 95 D 22.3125, lambda 0.50 to 0.70 by 0.02 (11 values) plus a repeat of 0.60, 4 processes at nice 15, beside part c2's leap (the order of the k_c 87 D 22.125 high scan)
NP=4; GATE=10; NICE=15
SRC=I1025-macm3/kc95_d223125/in
LAMP=("0.60" "0.60" "0.50" "0.52" "0.54" "0.56" "0.58" "0.62" "0.64" "0.66" "0.68" "0.70")
WIN="0.50 0.70"; REP=0.60
PENV
cmp -s <(grep -E '^(TAG|RAWC|STATEFILE|STATEBLOB|RECBLOB)=' $SCAN/point.env) <(grep -E '^(TAG|RAWC|STATEFILE|STATEBLOB|RECBLOB)=' $L/22.3125_kc95/point.env) || stop "the pins differ from the wide scan's point.env"
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
f=sol_${TAG}_D22.3125.npy
if [ -e $WTM5/data/$f ]; then [ "$(blob $WTM5/data/$f)" = "$(blob $SCAN/in/$f)" ] || stop "$WTM5/data/$f differs from the pinned state"; else cp $SCAN/in/$f $WTM5/data/$f; fi
[ -e $WTM5/data/${TAG}_asof_D$D.jsonl ] || cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (the same pinned state and record, blobs $(blob $SCAN/in/$f | cut -c1-8) and $(blob $SCAN/in/$TAG.jsonl | cut -c1-8), as the wide scan, whose regrid kc95_syscheck_1025.py accepted at 09:38:22 UTC with controls 1 1 and the k_c 87 refusal: $F/regrid/syscheck.txt)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC verdict: $(cut -c1-30 $SCAN/VERDICT.txt) (high95.sh)" >> $SCAN/steps.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (k_c 95 high scan)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "high scan starts (point87.sh $DN scan)"
bash $L/point87.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
( cd $IN && D18_DIR=$IN $PY -I wide_read.py $SCAN/read_lower.txt > $SCAN/wide_read.txt 2>&1 )
cp $SCAN/wide_read.txt $F/wide_read_high.txt; cp $SCAN/read_lower.txt $F/read_lower_high.txt
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 95) high scan done" > /dev/null 2>&1; bash $F/push95.sh "kc95_d223125: high scan reading" > /dev/null 2>&1
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(' $SCAN/wide_read.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc95_d223125: the k_c 95 D 22.3125 HIGH SCAN (0.50 to 0.70) is read: $(grep -E '^hybrid signs|^robust changes|change ' $SCAN/wide_read.txt | tr '\n' ';' | cut -c1-900) (full table follows in my report; raw kc87_leg_lambda/$DN/ and kc95_d223125/)"
exit 0
}
