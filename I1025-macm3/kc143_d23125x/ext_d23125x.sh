#!/bin/bash
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
# 6. the scan folder (pins from the pushed commit), the lock, then point87.sh scan
RAWC=$(grep '^RAWC=' $L/$MAIN/point.env | cut -d= -f2); [ -n "$RAWC" ] || stop "no RAWC in $L/$MAIN/point.env"
git -C $RAWG cat-file -e $RAWC:I1025-macm3/$(basename $F)/in/$TAG.jsonl 2>/dev/null || stop "the pushed commit $RAWC does not hold the regrid record"
mkdir -p $SCAN
{ cat <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=sol_${TAG}_$DT.npy
STATEBLOB=$(blob $IN/sol_${TAG}_$DT.npy | cut -c1-8)
RECBLOB=$(blob $IN/$TAG.jsonl | cut -c1-8)
SRC=I1025-macm3/$(basename $F)/in
PENV
  cat $KX/scan_plan_ext_$SIDE.env; } > $SCAN/point.env
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
for f in sol_${TAG}_$DT.npy; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
echo "ACCEPTED $(stamp) UTC (inherited from the lane: $(cat $OUT/VERDICT.txt); the k_c 143 regrid check of the lane, $OUT/syscheck.txt)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (ext_d23125x.sh): the lane's regrid verdict, $(cat $OUT/VERDICT.txt); the extension scan (side $SIDE) of the main scan $MAIN: $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)" >> $SCAN/steps.txt
[ "$TESTMODE" = dry ] && { bash $L/pointnew_rs.sh $DN dry > $SCAN/dry.txt 2>&1; say "dry: pointnew_rs.sh dry exit $? ($(tail -1 $SCAN/dry.txt))"; exit 0; }
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (extension scan, side $SIDE)" > /dev/null 2>&1
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "scan starts (pointnew_rs.sh $DN scan: the scanner d18_secant.py scan with --b12=rust --b12_threads=4)"
bash $L/pointnew_rs.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 143, extension scan) scan done" > /dev/null 2>&1
nch=$(grep -c 'robust change (' $SCAN/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCAN/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^repeated|^float64' $SCAN/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc143_d23125x: the k_c 143 D 23.125 EXTENSION scan (side $SIDE) is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCAN/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DN/)"
[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1025 kc143_d23125x: the EXTENSION scan (side $SIDE) reads $nrb robust changes (one wanted): no secant refinement; stopped, your word"; exit 0; }
# 7. the secant refinement of the one robust change
BR=$(grep 'robust change (' $SCAN/read_lower.txt | sed -E 's/.*robust change \((-?[0-9.]+), (-?[0-9.]+)\).*/\1 \2/')
LO=${BR% *}; HI=${BR#* }
S_STATE=$SCAN/in/sol_${TAG}_$DT.npy; S_REC=$SCAN/in/$TAG.jsonl; SB=$(blob $S_STATE | cut -c1-8); TB=$(blob $S_REC | cut -c1-8)
mkdir -p $SEC; [ -e $SEC/secant.jsonl ] && stop "$SEC/secant.jsonl exists"
say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4"
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $SEC/samples.csv
( cd $WTS && env PYTHONPATH=$SITE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTS/d18_secant.py run $S_REC $S_STATE $D $LO $HI $SEC/secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4 > $SEC/secant.log 2>&1; echo $? > $SEC/exit.txt ) &
sp=$!
( while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*kc143_d23125x/secant"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $SEC/samples.csv; done; sleep 60; done ) &
wait $sp; se=$(cat $SEC/exit.txt)
say "secant exit $se"
[ "$se" = 0 ] || [ "$se" = 4 ] || stop "d18_secant.py exit $se (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $SEC/secant.log"
$PY $F/summarize_point.py $SCAN $SEC > $F/point_summary.txt 2>&1
bash $F/push_kc143_d23125x.sh "kc143_d23125x: D 23.125 scanned and its root refined (secant)" > /dev/null 2>&1
tell "macm3 #1025 kc143_d23125x done: [extension scan, side $SIDE; the window of the lane read no robust change] $(grep -E '^(scan:|secant: status|secant root)' $F/point_summary.txt | tr '\n' ';' | cut -c1-1400) (raw kc143_d23125x/ and kc87_leg_lambda/$DN/)"
exit 0
}
