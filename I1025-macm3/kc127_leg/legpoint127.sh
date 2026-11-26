#!/bin/bash
# #1025 macm3 kc127_leg (t5's order, hc 26 Nov ~15:23 UTC by t5's clock): the new point of the k_c 127 leg (D 23.125): wait for the leap's point (ready_D<D>.txt) and the end of the leap lane (one k_c 127 job at a time), pin its state and the record from the pushed
# commit (prepare87.sh), accept it (kc127_syscheck_1025.py exit 0, controls --mutate=F and --mutate=steps exit 1 1, the k_c 119 and k_c 111 checks refuse it), scan lambda -0.06, -0.05, -0.04, -0.03, -0.02 plus a repeat of -0.04 with the NEW scanner
# (d18_secant.py scan, wip/ell1-speed 92b9bf53, eb1396ad) on 2 processes (kc87_leg_lambda/pointnew.sh, folder kc87_leg_lambda/<D>_kc127/), read by read_lower.py and repeat_check.py; with exactly one robust change its bracket goes to d18_secant.py run
# (the same worktree, --tol=1e-5 --maxev=10 --pin=<state blob>,<record blob>, one process, folder kc127_leg/secant_D<D>/); summarize_point.py prints the numbers. Stops (hc to t5): the guard stopped the leap (the point is then scanned only if the leap wrote it), no ready file,
# acceptance not as written, a pin, a scan without SCAN_DONE.txt, no or several robust changes (reported, not widened), a secant exit other than 0 or 4. usage: bash legpoint127.sh D [dry]
{
D=${1:?D, e.g. 23.125}; MODE=${2:-}
K=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc127_leg; L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
WTM3=$HOME/Source/choptuik-large-d-1025m3/solver/matter; WTM5=$HOME/Source/choptuik-large-d-1025m/solver/matter; WTS=$HOME/Source/choptuik-large-d-1025s2/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc127Lmacm3; DT=$(printf "D%.6f" $D); DN=${D}_kc127; SCAN=$L/$DN; SEC=$K/secant_D$D; STATEFILE=sol_${TAG}_$DT.npy
LOGF=$K/exits_leg127.txt; HC=$(command -v hc)
stamp() { date -u '+%F %T'; }
say() { echo "kc127_leg point $D: $* $(stamp) UTC" | tee -a $LOGF; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOGF 2>&1; }
stop() { tell "macm3 #1025 kc127_leg point D $D STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
export PYTHONDONTWRITEBYTECODE=1
cd $K || exit 9
# 1. the leap's point
say "waiting for ready_D$D.txt"
until [ -e $K/ready_D$D.txt ] && grep -q "point D $D: pushed" $LOGF; do
  pgrep -f 'kc127_leg/run_leg127.sh' > /dev/null || { [ -e $K/ready_D$D.txt ] && grep -q "point D $D: pushed" $LOGF && break; stop "the leap lane is gone and D $D has no ready file or no pushed line"; }
  sleep 30
done
RAWC=$(grep "point D $D: pushed" $LOGF | head -1 | sed 's/.*pushed \([0-9a-f]*\).*/\1/')
RECBLOB=$(git -C $RAWG rev-parse --short=8 $RAWC:I1025-macm3/kc127_leg/states/$TAG.jsonl 2>/dev/null); STATEBLOB=$(git -C $RAWG rev-parse --short=8 $RAWC:I1025-macm3/kc127_leg/states/$STATEFILE 2>/dev/null)
[ -n "$RECBLOB" ] && [ -n "$STATEBLOB" ] || stop "the pushed commit $RAWC does not hold the point's state and record"
say "the point is pushed (raw $RAWC): state $STATEFILE $STATEBLOB, record $TAG.jsonl $RECBLOB"
while pgrep -f 'kc127_leg/run_leg127.sh' > /dev/null; do sleep 20; done      # the leap lane has ended (one k_c 127 job at a time)
if [ -e $K/leg_STOP.txt ]; then   # t5: "Stop and report on: the guard firing (report its line; do not force the step)"
  tell "macm3 #1025 kc127_leg: the guard fired: $(head -1 $K/leg_STOP.txt | cut -c1-200); the point D $D was written and pushed (raw $RAWC) before the stop; I do not scan or refine it until you say so (the guard's row is in leg_points.txt)"; exit 0
fi
# 2. the scan folder and the pins
mkdir -p $SCAN
cat > $SCAN/point.env <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=$STATEFILE
STATEBLOB=$STATEBLOB
RECBLOB=$RECBLOB
# t5's order (hc 25 Nov ~22:55 UTC): scan each new point of macm3's k_c 103 leg on -0.10 to 0.02 by 0.02, plus a repeat of -0.04 (8 evaluations; central values first, around the predicted -0.025)
NP=2; GATE=10; NICE=15
SRC=I1025-macm3/kc127_leg/states
LAMP=("-0.04" "-0.04" "-0.03" "-0.05" "-0.02" "-0.06")
WIN="-0.06 -0.02"; REP=-0.04
PENV
bash $L/prepare87.sh $DN > $SCAN/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SCAN/prepare.log)"
# 3. acceptance on the pinned copies
STATE=$SCAN/in/$STATEFILE; REC=$SCAN/in/$TAG.jsonl; OUT=$SCAN/accept; mkdir -p $OUT
C127="nice -n 10 $PY -I $K/in/kc127_syscheck_1025.py $REC $STATE $D $WTM3"
$C127 > $OUT/syscheck.txt 2>&1; c0=$?; $C127 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; c1=$?; $C127 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; c2=$?
nice -n 10 $PY -I $K/in/kc119_syscheck_1025.py $REC $STATE $D $WTM3 > $OUT/syscheck_kc119_refuses.txt 2>&1; c3=$?
nice -n 10 $PY -I $K/in/kc111_syscheck_1025.py $REC $STATE $D $WTM3 > $OUT/syscheck_kc111_refuses.txt 2>&1; c4=$?
say "acceptance: kc127_syscheck exit $c0 (0 wanted); controls --mutate=F $c1, --mutate=steps $c2 (1 wanted each); kc119_syscheck $c3 and kc111_syscheck $c4 on the new state (1 wanted each): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-300)"
[ "$c0 $c1 $c2 $c3 $c4" = "0 1 1 1 1" ] || { echo "REFUSED: kc127 $c0, controls $c1 $c2, kc119 $c3, kc111 $c4" > $SCAN/VERDICT.txt; stop "the new state is not accepted as written (exits $c0 $c1 $c2 $c3 $c4; wanted 0 1 1 1 1)"; }
echo "ACCEPTED $(stamp) UTC (kc127_syscheck_1025.py of the leg lane, $OUT; controls and the k_c 119 and k_c 111 refusals there)" > $SCAN/VERDICT.txt
echo "$(stamp) UTC accept (legpoint127.sh): kc127 exit $c0, controls $c1 $c2, kc119 $c3, kc111 $c4" >> $SCAN/steps.txt
for f in $STATEFILE; do cp $SCAN/in/$f $WTM5/data/$f; done; cp $SCAN/in/$TAG.jsonl $WTM5/data/${TAG}_asof_D$D.jsonl
[ "$MODE" = dry ] && { say "dry run: pins and acceptance passed; nothing scanned"; exit 0; }
bash $L/push87.sh "kc87_leg_lambda: D $DN pins and verdict (k_c 127 leg)" > /dev/null 2>&1
# 4. the scan (2 processes while the leap or a secant run is alive)
while pgrep -f 'kc127_leg/run_leg127.sh' > /dev/null; do sleep 20; done      # one k_c 127 job at a time (t5)
export NP=2
echo "NP=$NP" >> $SCAN/point.env
LOCK=$L/.scan.lock; n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && stop "the scan lock stayed busy for 15 h"; sleep 20
done
echo $$ > $LOCK.pid
say "scan starts (pointnew.sh $DN scan: the new scanner d18_secant.py scan, $NP processes)"
bash $L/pointnew.sh $DN scan >> $SCAN/pipeline.log 2>&1; sc=$?
rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null
say "scan exit $sc"
[ -e $SCAN/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCAN/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DN (k_c 127 leg) scan done" > /dev/null 2>&1
nch=$(grep -c 'robust change (' $SCAN/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCAN/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^repeated|^float64' $SCAN/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1025 kc127_leg point D $D: the scan is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCAN/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DN/)"
[ "$nch" = 1 ] && [ "$nrb" = 1 ] || { tell "macm3 #1025 kc127_leg point D $D: the scan reads $nrb robust changes (one wanted): no secant refinement; reported, the window is not widened"; exit 0; }
# 5. the secant refinement of the one robust change
BR=$(grep 'robust change (' $SCAN/read_lower.txt | sed -E 's/.*robust change \((-?[0-9.]+), (-?[0-9.]+)\).*/\1 \2/')
LO=${BR% *}; HI=${BR#* }
[ "$(git -C ${WTS%/solver/matter} rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTS/d18_secant.py)" = eb1396ad ] || stop "the scanner/secant worktree or d18_secant.py blob is not as pinned (92b9bf53, eb1396ad)"
mkdir -p $SEC; [ -e $SEC/secant.jsonl ] && stop "$SEC/secant.jsonl exists"
say "secant starts: d18_secant.py run $REC $STATE $D $LO $HI secant.jsonl --tol=1e-5 --maxev=10 --pin=$STATEBLOB,$RECBLOB"
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $SEC/samples.csv
( cd $WTS && env RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u $K/in/capped_run.py 18000 $PY -u $WTS/d18_secant.py run $REC $STATE $D $LO $HI $SEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=$STATEBLOB,$RECBLOB > $SEC/secant.log 2>&1; echo $? > $SEC/exit.txt ) &
sp=$!
( while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*secant_D$D"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')" >> $SEC/samples.csv; done; sleep 60; done ) &
wait $sp; se=$(cat $SEC/exit.txt)
say "secant exit $se"
[ "$se" = 0 ] || [ "$se" = 4 ] || stop "d18_secant.py exit $se (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $SEC/secant.log"
$PY $K/summarize_point.py $SCAN $SEC > $K/point_D${D}_summary.txt 2>&1
bash $K/push_leg127.sh "kc127_leg: D $D scanned and its root refined (secant)" > /dev/null 2>&1
tell "macm3 #1025 kc127_leg point D $D done: $(grep -E '^(scan:|secant: status|secant root|secant root inside)' $K/point_D${D}_summary.txt | tr '\n' ';' | cut -c1-1400) (raw kc127_leg/ and kc87_leg_lambda/$DN/)"
exit 0
}
