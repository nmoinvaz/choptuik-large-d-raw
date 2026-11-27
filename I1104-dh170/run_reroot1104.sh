#!/bin/bash
# #1104's second run (t5's order, comment 7226665371): re-root macm3's k_c 127 D 23.125 state at kappa 0.7 on the Rust block 12 at lambda -0.045 and -0.040 (one process each, 1 thread,
# nice 19: R2's secant keeps priority), then `run` at tol 5e-5 on the robust change (--ends takes the scan's two end records), then the reading of the pair.
# usage: run_reroot1104.sh [LAMS]        (default -0.045,-0.040)   Stops at the first failure (STOP_reroot.txt); DONE_reroot.txt when it ends.
{
LAMS=${1:--0.045,-0.040}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1104-dh170
WT=/home/nathan/Source/choptuik-large-d-1101k
WTM=$WT/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.125; NI=19
SF=in/sol_l1kc127Lmacm3_D23.1250.npy; RF=in/l1kc127Lmacm3.jsonl; SB=e1dccb3c; RB=58d3b080
TAG=reroot
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = f56f91d2 ] && [ -z "$(git -C $WT status --short solver | head -1)" ] || stop "the scanner worktree is not f56f91d2 or not clean"
[ "$(blob $WTM/d18_secant.py)" = 2f3ee874 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py is not 2f3ee874 or ell_b12rs.py not a1fff74f"
[ "$(blob $SF)" = $SB ] && [ "$(blob $RF)" = $RB ] || stop "the source state or record is not the pinned blob ($SB, $RB)"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] && [ "$(blob results_1104.py)" = a1dd91ba ] || stop "read_lower.py, its change finder or results_1104.py is not the pinned blob"
[ -e scan_070/scan_D23.125_p0.jsonl ] && stop "scan_070/scan_D23.125_p0.jsonl exists: not overwriting"
step "pins ok: scanner worktree f56f91d2 (d18_secant.py 2f3ee874, ell_b12rs.py a1fff74f), source $SB / $RB, read_lower.py 89309d3c, results_1104.py a1dd91ba; lambdas $LAMS, nice $NI"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
cd $WTM
nice -n $NI $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant_reroot.txt 2>&1; e0=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_reroot_half.txt 2>&1; e1=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_reroot_norobust.txt 2>&1; e2=$?
nice -n $NI $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_reroot_nosigncheck.txt 2>&1; e3=$?
cd $OUT
step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
r0=0; r1=0; r2=0
$PY -I results_1104.py selftest > selftests/selftest_results_1104_drv_reroot.txt 2>&1 || r0=1
$PY -I results_1104.py selftest --mutate=sign > selftests/selftest_results_1104_drv_reroot_sign.txt 2>&1 && r1=1
$PY -I results_1104.py selftest --mutate=bar > selftests/selftest_results_1104_drv_reroot_bar.txt 2>&1 && r2=1
step "results_1104.py selftest ok=$((1 - r0)) (1 wanted); mutations sign and bar both fail=$((2 - r1 - r2)) (2 wanted)"
[ $r0 = 0 ] && [ $r1 = 0 ] && [ $r2 = 0 ] || stop "a results_1104.py selftest or mutation did not read as written"
step "scan starts: D $D, lambda $LAMS, one process per lambda, 1 thread each, nice $NI, --b12=rust --b12_threads=1"
t0=$(date +%s); pids=(); i=0
for L in ${LAMS//,/ }; do
  ( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $L $OUT/scan_070/scan_D23.125_p$i.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/scan_070_p$i.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $L exit $rc" >> $OUT/steps.txt ) &
  pids+=($!); i=$((i+1))
done
# the pilot stop condition: every scan prints its record-system line (or fails the check) within 40 min
for n in $(seq 1 120); do
  k=$(grep -l -E 'the record system' scan_070_p*.raw 2>/dev/null | wc -l); [ "$k" = "$i" ] && break; sleep 20
done
grep -h 'the record system' scan_070_p*.raw > recsys_070.txt 2>&1
step "record-system lines: $(grep -c 'NOT the record system' recsys_070.txt) NOT, $(grep -c ': the record system' recsys_070.txt) of $i ok: $(head -1 recsys_070.txt | cut -c1-200)"
if [ "$(grep -c 'NOT the record system' recsys_070.txt)" != 0 ] || [ "$(grep -c ': the record system' recsys_070.txt)" != "$i" ]; then
  pkill -f "d18_secant.py scan $OUT/$RF" ; wait "${pids[@]}"
  stop "a scan did not print the record system (recsys_070.txt); the scans were killed"
fi
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for f in scan_070_p*.raw; do grep -hE 'the record system|block 12 by ellrs|Elapsed|Maximum resident' $f | head -4 >> steps.txt; done
( cd in; lo=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | head -1); hi=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | tail -1)
  { echo "== reroot: read_lower.py scan_070 $lo $hi"; $PY -I read_lower.py $OUT/scan_070 $lo $hi; echo "(exit $?)"; } > $OUT/read_lower_070.txt 2>&1 )
$PY -I results_1104.py scan scan_070 > results_070.md 2> results_070.err; rc=$?
step "results_1104.py scan exit $rc (0 a bracket, 2 no robust change), results_070.md"
if [ $rc = 2 ]; then echo "reroot DONE $(stamp) UTC, no robust change in the scan (report and wait)" > DONE_reroot.txt; step "done: no robust change, no secant (report and wait)"; exit 0; fi
[ $rc = 0 ] || stop "results_1104.py scan exit $rc"
PAIR=$($PY -I results_1104.py scan scan_070 --pair); LO=${PAIR% *}; HI=${PAIR#* }
cat scan_070/scan_D23.125_p*.jsonl > scan_070_all.jsonl
step "secant starts: d18_secant.py run $RF $SF $D $LO $HI secant_070.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=scan_070_all.jsonl --pin=$SB,$RB"
t0=$(date +%s)
( cd $WTM && PYTHONPATH=$SITE nice -n $NI /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/$RF $OUT/$SF $D $LO $HI $OUT/secant_070.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=$OUT/scan_070_all.jsonl --pin=$SB,$RB > $OUT/secant_070.log 2>&1 )
rs=$?
step "secant exit $rs (0 tol, 4 maxev or non-robust, 2 refused, 3 not the record system), $(( $(date +%s) - t0 )) s; $(tail -1 secant_070.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
echo "reroot DONE $(stamp) UTC, secant exit $rs" > DONE_reroot.txt
step "done"
exit 0
}
