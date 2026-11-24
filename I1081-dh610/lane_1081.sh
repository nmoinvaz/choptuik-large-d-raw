#!/bin/bash
# #1081 dh610 lane: pins and selftests, then 24 jobs (3 point runs, 21 box runs: per configuration a, b, c one point run, one unperturbed box run, six box runs under review_1079/perturb_box.py with REVIEW_PERTURB=qr
# REVIEW_SEED=1..6) over a pool of 5 processes of 1 thread at nice 10, then certify_M.py krawczyk --point --box for every box (and controls on each U) at the configuration's CERTIFY_M_PREC, then the summary.
# Memory: refuses to start with less than 24 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): the sampler only writes MEMALERT_1081.txt below 4 GiB.
# usage: bash lane_1081.sh [dry]
{
set -u
MODE=${1:-}
. $(dirname $0)/common.sh
L=$F/exits_1081.txt; NP=5
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC I1081 lane: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
bad=0
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain)" ] || { say "refuse: $W is not at $BR or is not clean"; bad=1; }
while read bb f; do [ -f $F/in/$f ] && [ "$(hb $F/in/$f)" = "$bb" ] || { say "refuse: $F/in/$f missing or not blob $bb"; bad=1; }; done < $F/in_blobs.txt
[ "$(wc -l < $F/in_blobs.txt)" = 1 ] || { say "refuse: in_blobs.txt does not list exactly the refine file"; bad=1; }
grep -q 'CERTIFY_M_PREC' $W/solver/proof/certify_M.py || { say "refuse: certify_M.py has no CERTIFY_M_PREC"; bad=1; }
[ -f $W/solver/proof/review_1079/perturb_box.py ] || { say "refuse: perturb_box.py missing"; bad=1; }
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge 25165824 ] || { say "refuse: MemAvailable $av kB is below 24 GB"; bad=1; }
if [ "$MODE" != dry ]; then for c in a b c; do [ ! -e $F/cfg_$c ] || { say "refuse: $F/cfg_$c exists"; bad=1; }; done; fi
[ $bad = 0 ] || exit 1
$PY -I $F/summarize_1081.py selftest > $F/selftest_summarize.txt 2>&1; s1=$?
$PY -I $F/summarize_1081.py selftest --mutate > $F/selftest_summarize_mutate.txt 2>&1; s2=$?
[ $s1 = 0 ] && [ $s2 = 1 ] || stop "summarizer selftest $s1 (0 wanted), selftest --mutate $s2 (1 wanted)"
say "pins checked (worktree $W at $BR clean, refine file blob $(cut -c1-8 $F/in_blobs.txt), $($PY -V 2>&1), python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), MemAvailable $av kB, load $(cut -d' ' -f1-3 /proc/loadavg)); summarizer selftest $s1 and --mutate $s2 (0 1 wanted); 24 jobs over $NP processes"
JOBS="b point
b U
b s1
b s2
b s3
b s4
b s5
b s6
c point
c U
c s1
c s2
c s3
c s4
c s5
c s6
a point
a U
a s1
a s2
a s3
a s4
a s5
a s6"
if [ "$MODE" = dry ]; then say "dry run: nothing started; the job list is: $(echo "$JOBS" | tr '\n' ';')"; exit 0; fi
mkdir -p $F/cfg_a/logs $F/cfg_b/logs $F/cfg_c/logs
( sleep 5; while pgrep -f "^$PY (certify_M.py (box|point)|review_1079/perturb_box.py box)" > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    rs=$(ps -o rss= -p $(pgrep -f "^$PY (certify_M.py (box|point)|review_1079/perturb_box.py box)" | tr '\n' ',' | sed 's/,$//') 2>/dev/null | awk '{s+=$1} END {print s+0}')
    echo "$(date -u '+%F %T') UTC alive $(pgrep -fc "^$PY (certify_M.py (box|point)|review_1079/perturb_box.py box)"), RSS_kB $rs, MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg)" >> $F/sampler.log
    [ "$avs" -ge 4194304 ] || echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only)" >> $F/MEMALERT_1081.txt
    sleep 30
  done ) &
SAMP=$!
say "pool starts: 24 jobs, $NP processes of 1 thread, nice 10, cap 10800 s per job by timeout; order b, c, a (point, U, s1 to s6 of each)"
echo "$JOBS" | xargs -P $NP -L 1 bash $F/job.sh; px=$?
n=$(ls $F/cfg_?/point.json $F/cfg_?/box_*.json 2>/dev/null | wc -l)
say "pool ended: xargs exit $px (0 wanted), $n of 24 output files"
kill $SAMP 2>/dev/null
[ $px = 0 ] && [ "$n" = 24 ] || stop "a job failed (xargs exit $px, $n of 24 files); see steps.txt"
cd $W/solver/proof || exit 1
export PYTHONDONTWRITEBYTECODE=1
for c in a b c; do
  cfg $c; D=$F/cfg_$c; export CERTIFY_M_PREC=$PREC
  for r in U s1 s2 s3 s4 s5 s6; do
    $PY certify_M.py krawczyk --point=$D/point.json --box=$D/box_$r.json > $D/krawczyk_$r.log 2>&1; k=$?
    echo "exit $k" > $D/krawczyk_$r.exit
    echo "$(stamp) krawczyk $c $r exit $k: $(head -n 1 $D/krawczyk_$r.log | cut -c1-200)" >> $H
  done
  $PY certify_M.py controls --box=$D/box_U.json --point=$D/point.json > $D/controls_U.log 2>&1; k=$?
  echo "exit $k" > $D/controls_U.exit
  echo "$(stamp) controls $c U exit $k (0 wanted): $(tail -n 1 $D/controls_U.log | cut -c1-120)" >> $H
done
unset CERTIFY_M_PREC
say "krawczyk stage done: 21 Krawczyk tests and 3 controls (exit codes in cfg_*/krawczyk_*.exit and controls_U.exit, margins in steps.txt)"
[ -z "$(git -C $W status --porcelain)" ] || say "WARNING: the worktree $W is no longer clean: $(git -C $W status --porcelain | head -n 3 | tr '\n' ' ')"
cd $F
$PY -I summarize_1081.py > summary_1081.txt 2> summary_1081.err; a1=$?
$PY -I summarize_1081.py --mutate > summary_1081_mutate.txt 2>&1; a2=$?
say "summary exit $a1 (0 wanted); summarize --mutate exit $a2 (1 wanted; the control prints FIRED)"
say "lane done; tables in summary_1081.txt"
exit 0
}
