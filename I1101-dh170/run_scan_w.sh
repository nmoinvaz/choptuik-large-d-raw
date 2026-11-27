#!/bin/bash
# #1101 dh170, R2's widened scan (t5's order, comment 7218045186): R2's state at lambda 0.085, 0.100, 0.130 and 0.035, d18_secant.py scan --b12=rust --b12_threads=1, one process each, nice 10;
# then, if the eight points (this scan and scan_r2/) have a robust sign change, d18_secant.py run on the first one at tol 5e-5, then delta, E_root and the verdict (results_1101.py r2w).
# Starts when step 1d's four roots of #1105 have ended (DONE_c150, DONE_c165w, DONE_r150, DONE_r165w in I1105-dh170/step1d; a STOP_ file counts as ended) and none of them was refused;
# a refused one writes HOLD_r2w.txt and nothing starts. Needs GATES_DONE.txt and DONE_r2.txt.
# usage: run_scan_w.sh        Output: scan_r2w/scan_D23.0_p<i>.jsonl, scan_r2w_p<i>.raw, scan_r2all/ (the eight points), read_lower_r2w.txt, results_r2w.md, secant_r2w.jsonl/.log, results_r2w_secant.md, DONE_r2w.txt
{
TAG=r2w; LAMS=0.085,0.100,0.130,0.035
SF=in/sol_l1kc127k035w2_D23.0000.npy; RF=in/l1kc127k035w2.jsonl; SB=25ba3a91; RB=9111bfca
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
D1=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1d
WTM=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.0
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ -f GATES_DONE.txt ] && [ -f DONE_r2.txt ] || stop "GATES_DONE.txt or DONE_r2.txt is missing"
[ "$(git -C $WTM rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ "$(blob $WTM/d18_secant.py)" = 9706e506 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "the worktree is not d4b6b6ce or the scanner is not 9706e506"
[ "$(blob $SF)" = "$SB" ] && [ "$(blob $RF)" = "$RB" ] || stop "$SF or $RF is not the pinned blob ($SB, $RB)"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] || stop "the reader or its change finder is not the pinned blob"
[ "$(blob results_1101.py)" = 0ee6b8bf ] || stop "results_1101.py is not 0ee6b8bf"
step "pins ok: state $(blob $SF) record $(blob $RF); d18_secant.py 9706e506, ell_b12rs.py a1fff74f at d4b6b6ce; read_lower.py 89309d3c; results_1101.py 0ee6b8bf; lambdas $LAMS; waiting for step 1d's four roots"
ended() { for t in c150 c165w r150 r165w; do [ -f $D1/DONE_$t.txt ] || [ -f $D1/STOP_$t.txt ] || return 1; done; return 0; }
until ended; do sleep 20; done
for f in $D1/root_c150.jsonl $D1/root_c165w.jsonl $D1/root_r150.jsonl $D1/root_r165w.jsonl; do
  if jq -e 'select(.kind=="root" and .status=="refused")' $f > /dev/null 2>&1; then echo "HOLD $(stamp) UTC: $f was refused; nothing started" > $OUT/HOLD_$TAG.txt; step "HOLD: $f was refused"; exit 0; fi
done
step "step 1d's four roots ended ($(for t in c150 c165w r150 r165w; do cat $D1/DONE_$t.txt 2>/dev/null | cut -c1-60; done | tr '\n' ';'))"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
mkdir -p selftests
e=""; for m in "" shift signs e16 last; do
  if [ -z "$m" ]; then $PY -I results_1101.py selftest > selftests/selftest_results_w_run.txt 2>&1; else $PY -I results_1101.py selftest --mutate=$m > selftests/selftest_results_w_run_$m.txt 2>&1; fi; e="$e $?"
done
step "results_1101.py selftest exits (plain, shift, signs, e16, last):$e (0 1 1 1 1 wanted)"
[ "$e" = " 0 1 1 1 1" ] || stop "a results_1101.py selftest or mutation did not read as written"
mkdir -p scan_$TAG
step "scan starts: D $D, lambda $LAMS, one process per lambda, 1 thread each, nice 10, --b12=rust --b12_threads=1"
t0=$(date +%s); pids=(); i=0
for L in ${LAMS//,/ }; do
  ( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $L $OUT/scan_$TAG/scan_D23.0_p$i.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/scan_${TAG}_p$i.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $L exit $rc" >> $OUT/steps.txt ) &
  pids+=($!); i=$((i+1))
done
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for f in scan_${TAG}_p*.raw; do grep -h 'the record system\|NOT the record system\|block 12 by ellrs' $f | head -3 >> steps.txt; grep -hE 'Elapsed|Maximum resident' $f >> steps.txt; done
grep -l 'NOT the record system' scan_${TAG}_p*.raw && stop "a scan did not reproduce the record system"
[ "$(cat scan_$TAG/scan_D23.0_p*.jsonl | wc -l)" = 4 ] || stop "the widened scan has not four records"
mkdir -p scan_r2all; k=0
for f in scan_r2/scan_D23.0_p*.jsonl scan_$TAG/scan_D23.0_p*.jsonl; do cp $f scan_r2all/scan_D23.0_p$k.jsonl; cmp $f scan_r2all/scan_D23.0_p$k.jsonl || stop "copy of $f differs"; k=$((k+1)); done
( cd in; { echo "== $TAG: read_lower.py scan_r2all 0.035 0.130 (the four points of scan_r2 and the four of scan_$TAG)"; $PY -I read_lower.py $OUT/scan_r2all 0.035 0.130; echo "(exit $?)"; } > $OUT/read_lower_$TAG.txt 2>&1 )
$PY -I results_1101.py r2w scan_r2 scan_$TAG > results_$TAG.md 2> results_$TAG.err; rc=$?
step "results_1101.py r2w exit $rc (results_$TAG.md; 2 no robust change, 3 a bracket and no secant yet)"
if [ $rc = 3 ]; then
  read LO HI < <($PY -I results_1101.py r2w scan_r2 scan_$TAG --pair)
  step "secant starts: d18_secant.py run $RF $SF $D $LO $HI secant_$TAG.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --pin=$SB,$RB"
  t1=$(date +%s)
  ( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/$RF $OUT/$SF $D $LO $HI $OUT/secant_$TAG.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/secant_$TAG.log 2>&1 )
  sr=$?
  step "secant exit $sr (0: tol reached; 4: maxev or non-robust interior; 2: refused; 3: not the record system), $(( $(date +%s) - t1 )) s; $(tail -1 secant_$TAG.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
  $PY -I results_1101.py r2w scan_r2 scan_$TAG --secant=secant_$TAG.jsonl > results_${TAG}_secant.md 2> results_${TAG}_secant.err; rc=$?
  step "results_1101.py r2w --secant exit $rc (results_${TAG}_secant.md; 0 formed, 4 not read)"
fi
echo "$TAG DONE $(stamp) UTC, results exit $rc" > $OUT/DONE_$TAG.txt
step "done"
exit 0
}
