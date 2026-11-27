#!/bin/bash
# #1101 Test K (t5's order, comment 7222591656): state B (R0's re-solve at kappa 0.7) scanned with d18_secant.py --kappa_mm=0.35 (the mode matrix on the RK steps of kappa 0.35,
# worktree wip/ell1-kappa-mm f56f91d2), --b12=rust --b12_threads=1, one process per lambda, nice 10, then `run` at tol 5e-5 on the first robust change.
# usage: run_scan_k.sh [LAMS]        (default 0.085,0.100,0.115,0.130)   Stops at the first failure (STOP_k.txt).
# Stages: pins; selftests (d18_secant.py 0 1 1 1, results_1101k.py 0 1 1 1); the k_c 31 controls (plain, --kappa_mm=0.7 bit for bit equal, --kappa_mm=0.35 moves ln|det|);
# the scan with the step-count check (kappa_mm line: 8351 +- 2%, else the scans are killed); read_lower; the secant (--ends takes the scan's two end records); the reading.
{
LAMS=${1:-0.085,0.100,0.115,0.130}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
WT=/home/nathan/Source/choptuik-large-d-1101k
WTM=$WT/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.0; KM=0.35
SF=in/sol_l1kc127k070w2_D23.0000.npy; RF=in/l1kc127k070w2.jsonl; SB=90d3e655; RB=d1a3a641
TAG=k
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = f56f91d2 ] && [ -z "$(git -C $WT status --short solver | head -1)" ] || stop "the worktree is not f56f91d2 or not clean"
[ "$(blob $WTM/d18_secant.py)" = 2f3ee874 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "d18_secant.py is not 2f3ee874 or ell_b12rs.py not a1fff74f"
[ "$(blob $SF)" = $SB ] && [ "$(blob $RF)" = $RB ] || stop "state B is not the pinned blob ($SB, $RB)"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] && [ "$(blob results_1101k.py)" = c31a27c3 ] || stop "read_lower.py, its change finder or results_1101k.py is not the pinned blob"
[ "$(blob in/sol_l1kc31r1025_D10.5000.npy)" = f07a8984 ] && [ "$(blob in/l1kc31r1025.jsonl)" = e5a87ec5 ] || stop "the k_c 31 inputs are not the pinned blobs"
step "pins ok: worktree f56f91d2 (d18_secant.py 2f3ee874, ell_b12rs.py a1fff74f), state B $SB / $RB, read_lower.py 89309d3c, results_1101k.py c31a27c3; kappa_mm $KM; lambdas $LAMS"
mkdir -p selftests scan_k ctl_k31
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
cd $WTM
nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant_k.txt 2>&1; e0=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_k_half.txt 2>&1; e1=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_k_norobust.txt 2>&1; e2=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_k_nosigncheck.txt 2>&1; e3=$?
cd $OUT
step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
r0=0; r1=0; r2=0
$PY -I results_1101k.py selftest > selftests/selftest_results_1101k_drv.txt 2>&1 || r0=1
$PY -I results_1101k.py selftest --mutate=ref > selftests/selftest_results_1101k_drv_ref.txt 2>&1 && r1=1
$PY -I results_1101k.py selftest --mutate=bar > selftests/selftest_results_1101k_drv_bar.txt 2>&1 && r2=1
step "results_1101k.py selftest ok=$((1 - r0)) (1 wanted); mutations ref and bar both fail=$((2 - r1 - r2)) (2 wanted)"
[ $r0 = 0 ] && [ $r1 = 0 ] && [ $r2 = 0 ] || stop "a results_1101k.py selftest or mutation did not read as written"
# k_c 31 controls (t5's test: --kappa_mm=0.7, the record's kappa, is bit-identical to the plain scan; 0.35 moves ln|det|)
K31="nice -n 10 $PY -u $WTM/d18_secant.py scan $OUT/in/l1kc31r1025.jsonl $OUT/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87"
t0=$(date +%s)
( cd $WTM && PYTHONPATH=$SITE $K31 $OUT/ctl_k31/plain.jsonl --b12=rust --b12_threads=1 --pin=f07a8984,e5a87ec5 > $OUT/ctl_k31/plain.raw 2>&1 ) &
p1=$!
( cd $WTM && PYTHONPATH=$SITE $K31 $OUT/ctl_k31/km07.jsonl --b12=rust --b12_threads=1 --kappa_mm=0.7 --pin=f07a8984,e5a87ec5 > $OUT/ctl_k31/km07.raw 2>&1 ) &
p2=$!
( cd $WTM && PYTHONPATH=$SITE $K31 $OUT/ctl_k31/km035.jsonl --b12=rust --b12_threads=1 --kappa_mm=0.35 --pin=f07a8984,e5a87ec5 > $OUT/ctl_k31/km035.raw 2>&1 ) &
p3=$!
wait $p1 $p2 $p3
step "k_c 31 controls done: $(( $(date +%s) - t0 )) s"
c=$($PY -I - <<'EOF'
import json
def ln(p):
    r = [json.loads(l) for l in open(p) if l.strip()]
    return r[-1]["ln"], r[-1]["sign"]
a, b, c = (ln(f"ctl_k31/{n}.jsonl") for n in ("plain", "km07", "km035"))
print(f"plain {a[0]!r} sign {a[1]:+.0f}; kappa_mm 0.7 {b[0]!r} sign {b[1]:+.0f} (bit for bit {a == b}); kappa_mm 0.35 {c[0]!r} sign {c[1]:+.0f} (ln shift {c[0] - a[0]:+.4f})")
print("PASS" if a == b and abs(c[0] - a[0]) > 1e-3 else "FAIL")
EOF
)
step "k_c 31 controls: $(echo "$c" | head -1)"
[ "$(echo "$c" | tail -1)" = PASS ] || stop "the k_c 31 controls did not read as written (0.7 bit for bit equal to plain, 0.35 moves ln|det| by more than 1e-3)"
step "scan starts: D $D, lambda $LAMS, one process per lambda, 1 thread each, nice 10, --b12=rust --b12_threads=1 --kappa_mm=$KM"
t0=$(date +%s); pids=(); i=0
for L in ${LAMS//,/ }; do
  ( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $L $OUT/scan_k/scan_D23.0_p$i.jsonl --b12=rust --b12_threads=1 --kappa_mm=$KM --pin=$SB,$RB > $OUT/scan_k_p$i.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $L exit $rc" >> $OUT/steps.txt ) &
  pids+=($!); i=$((i+1))
done
# the pilot stop condition: every scan prints its kappa_mm line (or fails the record-system check) within 40 min; the step count must be 8351 +- 2%
for n in $(seq 1 120); do
  k=$(grep -l -E 'kappa_mm [0-9.]+:|NOT the record system' scan_k_p*.raw 2>/dev/null | wc -l); [ "$k" = "$i" ] && break; sleep 20
done
$PY -I results_1101k.py steps scan_k_p*.raw > steps_check_k.txt 2>&1; es=$?
step "kappa_mm step-count check exit $es (0 wanted): $(head -1 steps_check_k.txt | cut -c1-300)"
if [ $es != 0 ]; then
  pkill -f "d18_secant.py scan $OUT/$RF" ; wait "${pids[@]}"
  stop "the kappa_mm step count is not 8351 +- 2% (steps_check_k.txt); the scans were killed"
fi
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for f in scan_k_p*.raw; do grep -h 'the record system\|NOT the record system\|block 12 by ellrs\|^kappa_mm' $f | head -4 >> steps.txt; grep -hE 'Elapsed|Maximum resident' $f >> steps.txt; done
grep -l 'NOT the record system' scan_k_p*.raw && stop "a scan did not reproduce the record system"
( cd in; lo=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | head -1); hi=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | tail -1)
  { echo "== k: read_lower.py scan_k $lo $hi"; $PY -I read_lower.py $OUT/scan_k $lo $hi; echo "(exit $?)"; } > $OUT/read_lower_k.txt 2>&1 )
$PY -I results_1101k.py scan scan_k > results_k.md 2> results_k.err; rc=$?
step "results_1101k.py scan exit $rc (2 no robust change, 3 a bracket, results_k.md)"
if [ $rc = 2 ]; then echo "k DONE $(stamp) UTC, no robust change in the scan" > DONE_k.txt; step "done: no robust change, no secant (report and wait)"; exit 0; fi
[ $rc = 3 ] || stop "results_1101k.py scan exit $rc"
PAIR=$($PY -I results_1101k.py scan scan_k --pair); LO=${PAIR% *}; HI=${PAIR#* }
cat scan_k/scan_D23.0_p*.jsonl > scan_kall.jsonl
step "secant starts: d18_secant.py run $RF $SF $D $LO $HI secant_k.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --kappa_mm=$KM --ends=scan_kall.jsonl --pin=$SB,$RB"
t0=$(date +%s)
( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py run $OUT/$RF $OUT/$SF $D $LO $HI $OUT/secant_k.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --kappa_mm=$KM --ends=$OUT/scan_kall.jsonl --pin=$SB,$RB > $OUT/secant_k.log 2>&1 )
rs=$?
step "secant exit $rs (0 tol, 4 maxev or non-robust, 2 refused, 3 not the record system), $(( $(date +%s) - t0 )) s; $(tail -1 secant_k.jsonl 2>/dev/null | jq -c 'select(.kind=="root") | {status,bracket,width,signs,robust,lam_lin,lam_brent,n_eval}' 2>/dev/null)"
$PY -I results_1101k.py scan scan_k --secant=secant_k.jsonl --r2=secant_r2w.jsonl > results_k_secant.md 2> results_k_secant.err; rr=$?
step "results_1101k.py with the secants exit $rr (0 formed, 4 a record not read: R2's secant may still run)"
echo "k DONE $(stamp) UTC, secant exit $rs, reading exit $rr" > DONE_k.txt
step "done"
exit 0
}
