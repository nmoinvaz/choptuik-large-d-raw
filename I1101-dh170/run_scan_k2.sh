#!/bin/bash
# #1101 Test K, extension (t5's order of 17:3x UTC 27 Nov, after the scan at 0.085-0.130 found no change): the same state B and the same scanner, --kappa_mm=0.35, at lambda
# 0.040, 0.055, 0.070 (below) and 0.150 (above, in case the orientation flipped), one process per lambda, 1 thread, nice 10, files scan_k/scan_D23.0_p4..p7 beside the first four
# (results_1101k.py reads all eight). Then `run` at tol 5e-5 on the first robust change of the eight points (lowest lambda), and the reading against R2's secant.
# usage: run_scan_k2.sh [LAMS]        (default 0.040,0.055,0.070,0.150)   Stops at the first failure (STOP_k2.txt).
# Stages: pins; selftests (d18_secant.py 0 1 1 1, results_1101k.py 0 1 1); the scan with the step-count check (kappa_mm line 8351 +- 2%, else the scans are killed); read_lower over
# 0.040-0.150; the reading of the eight points; the secant (--ends takes the scan's two end records); the reading with R2's secant. The k_c 31 controls are not repeated (same pinned code).
{
LAMS=${1:-0.040,0.055,0.070,0.150}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
WT=/home/nathan/Source/choptuik-large-d-1101k
WTM=$WT/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.0; KM=0.35; I0=4
SF=in/sol_l1kc127k070w2_D23.0000.npy; RF=in/l1kc127k070w2.jsonl; SB=90d3e655; RB=d1a3a641
TAG=k2
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = f56f91d2 ] && [ -z "$(git -C $WT status --short solver | head -1)" ] || stop "the worktree is not f56f91d2 or not clean"
[ "$(blob $WTM/d18_secant.py)" = 2f3ee874 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py is not 2f3ee874 or ell_b12rs.py not a1fff74f"
[ "$(blob $SF)" = $SB ] && [ "$(blob $RF)" = $RB ] || stop "state B is not the pinned blob ($SB, $RB)"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] && [ "$(blob results_1101k.py)" = c31a27c3 ] || stop "read_lower.py, its change finder or results_1101k.py is not the pinned blob"
[ -e scan_k/scan_D23.0_p4.jsonl ] && stop "scan_k/scan_D23.0_p4.jsonl exists: not overwriting"
step "pins ok: worktree f56f91d2 (d18_secant.py 2f3ee874, ell_b12rs.py a1fff74f), state B $SB / $RB, read_lower.py 89309d3c, results_1101k.py c31a27c3; kappa_mm $KM; lambdas $LAMS (files p$I0..)"
mkdir -p selftests scan_k
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
cd $WTM
nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant_k2.txt 2>&1; e0=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_k2_half.txt 2>&1; e1=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_k2_norobust.txt 2>&1; e2=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_k2_nosigncheck.txt 2>&1; e3=$?
cd $OUT
step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
r0=0; r1=0; r2=0
$PY -I results_1101k.py selftest > selftests/selftest_results_1101k_k2.txt 2>&1 || r0=1
$PY -I results_1101k.py selftest --mutate=ref > selftests/selftest_results_1101k_k2_ref.txt 2>&1 && r1=1
$PY -I results_1101k.py selftest --mutate=bar > selftests/selftest_results_1101k_k2_bar.txt 2>&1 && r2=1
step "results_1101k.py selftest ok=$((1 - r0)) (1 wanted); mutations ref and bar both fail=$((2 - r1 - r2)) (2 wanted)"
[ $r0 = 0 ] && [ $r1 = 0 ] && [ $r2 = 0 ] || stop "a results_1101k.py selftest or mutation did not read as written"
step "scan starts: D $D, lambda $LAMS, one process per lambda, 1 thread each, nice 10, --b12=rust --b12_threads=1 --kappa_mm=$KM"
t0=$(date +%s); pids=(); i=$I0; n=0
for L in ${LAMS//,/ }; do
  ( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $L $OUT/scan_k/scan_D23.0_p$i.jsonl --b12=rust --b12_threads=1 --kappa_mm=$KM --pin=$SB,$RB > $OUT/scan_k2_p$i.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $L exit $rc" >> $OUT/steps.txt ) &
  pids+=($!); i=$((i+1)); n=$((n+1))
done
# the pilot stop condition: every scan prints its kappa_mm line (or fails the record-system check) within 40 min; the step count must be 8351 +- 2%
for j in $(seq 1 120); do
  k=$(grep -l -E 'kappa_mm [0-9.]+:|NOT the record system' scan_k2_p*.raw 2>/dev/null | wc -l); [ "$k" = "$n" ] && break; sleep 20
done
$PY -I results_1101k.py steps scan_k2_p*.raw > steps_check_k2.txt 2>&1; es=$?
step "kappa_mm step-count check exit $es (0 wanted): $(head -1 steps_check_k2.txt | cut -c1-300)"
if [ $es != 0 ]; then
  pkill -f "d18_secant.py scan $OUT/$RF" ; wait "${pids[@]}"
  stop "the kappa_mm step count is not 8351 +- 2% (steps_check_k2.txt); the scans were killed"
fi
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for f in scan_k2_p*.raw; do grep -h 'the record system\|NOT the record system\|block 12 by ellrs\|^kappa_mm' $f | head -4 >> steps.txt; grep -hE 'Elapsed|Maximum resident' $f >> steps.txt; done
grep -l 'NOT the record system' scan_k2_p*.raw && stop "a scan did not reproduce the record system"
[ "$(ls scan_k/scan_D23.0_p*.jsonl | wc -l)" = 8 ] || stop "the eight scan files are not all there"
( cd in; lo=$(echo ${LAMS//,/ } 0.085 0.130 | tr ' ' '\n' | sort -g | head -1); hi=$(echo ${LAMS//,/ } 0.085 0.130 | tr ' ' '\n' | sort -g | tail -1)
  { echo "== k2: read_lower.py scan_k $lo $hi"; $PY -I read_lower.py $OUT/scan_k $lo $hi; echo "(exit $?)"; } > $OUT/read_lower_k2.txt 2>&1 )
$PY -I results_1101k.py scan scan_k > results_k2.md 2> results_k2.err; rc=$?
step "results_1101k.py scan (eight points) exit $rc (2 no robust change, 3 a bracket, results_k2.md)"
if [ $rc = 2 ]; then echo "k2 DONE $(stamp) UTC, no robust change in the eight points" > DONE_k2.txt; step "done: no robust change, no secant (report and wait)"; exit 0; fi
[ $rc = 3 ] || stop "results_1101k.py scan exit $rc"
PAIR=$($PY -I results_1101k.py scan scan_k --pair); LO=${PAIR% *}; HI=${PAIR#* }
cat scan_k/scan_D23.0_p*.jsonl > scan_kall.jsonl
step "secant starts: d18_secant.py run $RF $SF $D $LO $HI secant_k.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --kappa_mm=$KM --ends=scan_kall.jsonl --pin=$SB,$RB"
t0=$(date +%s)
( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/$RF $OUT/$SF $D $LO $HI $OUT/secant_k.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --kappa_mm=$KM --ends=$OUT/scan_kall.jsonl --pin=$SB,$RB > $OUT/secant_k.log 2>&1 )
rs=$?
step "secant exit $rs (0 tol, 4 maxev or non-robust, 2 refused, 3 not the record system), $(( $(date +%s) - t0 )) s; $(tail -1 secant_k.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
$PY -I results_1101k.py scan scan_k --secant=secant_k.jsonl --r2=secant_r2w.jsonl > results_k2_secant.md 2> results_k2_secant.err; rr=$?
step "results_1101k.py with the secants exit $rr (0 formed, 4 a record not read: R2's secant may still run)"
echo "k2 DONE $(stamp) UTC, secant exit $rs, reading exit $rr" > DONE_k2.txt
step "done"
exit 0
}
