#!/bin/bash
# #1025 kc119_d2225 step 3 (t5's order, 26 Nov): scan of the accepted k_c 119 state at D 22.25 with the NEW scanner, d18_secant.py scan (branch wip/ell1-speed, commit 92b9bf53, blob eb1396ad) from the worktree -1025sp, at lambda
# -0.04, -0.02, 0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12 and a repeat of 0.04 (10 evaluations), 3 single-thread processes at nice 10 in four rounds (the lists of stage.conf); the fast float64 matrix is the default, --pin the result's blobs.
# Before the first point: the worktree's pins, d18_secant.py selftest (exit 0) and its --mutate=half, norobust, nosigncheck (exit 1 each), logged with the blob. Memory: alert only. Then read_lower.py selftest (0), its mutations (1 each), the reader on the whole window
# -0.04 to 0.12 (a contiguous 0.02 grid) and repeat_check.py. Starts only after VERDICT.txt says ACCEPTED. usage: run_scan.sh [dry]. A systemd user unit (run by lane_k119.sh). This is kc119_d23_wide/run_scan.sh with the scanner, folder, lists and reading changed (run_scan_vs_kc119_d23_wide.diff).
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc119_d2225
WTS=/home/nathan/Source/choptuik-large-d-1025sp; WTSM=$WTS/solver/matter
MODE=${1:-}
OUT=$ROOT; IN=$OUT/in
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
[ -f $OUT/stage.conf ] || { echo "no $OUT/stage.conf"; exit 9; }
. $OUT/stage.conf
SCAN=$OUT/scan
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1"; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
while read -r h f; do [ "$(blob $IN/$f)" = "$h" ] || { step "SCAN STOP: in/$f is not blob $h"; exit 1; }; done < $OUT/in_blobs.txt
STATE=$OUT/sol_${TAG}_${DT}.npy; STUB=$OUT/$TAG.jsonl
[ -s $STATE ] && [ -s $STUB ] && [ -s $WTM/data/sol_${TAG}_${DT}.npy ] && [ -s $WTM/data/$TAG.jsonl ] || { step "SCAN STOP: the accepted state or record is missing or empty"; exit 1; }
[ "$(blob $STATE)" = "$(blob $WTM/data/sol_${TAG}_${DT}.npy)" ] && [ "$(blob $STUB)" = "$(blob $WTM/data/$TAG.jsonl)" ] || { step "SCAN STOP: the accepted state or record differs from the worktree's"; exit 1; }
[ -e $SCAN ] && [ "$MODE" != dry ] && { step "SCAN STOP: $SCAN exists"; exit 1; }
NP=${#LAMP[@]}
# the new scanner: worktree -1025sp at 92b9bf53, d18_secant.py blob eb1396ad (= in/d18_secant.py), dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399
[ "$(git -C $WTS rev-parse --short=8 HEAD)" = 92b9bf53 ] || { step "SCAN STOP: the scanner worktree is not at 92b9bf53"; exit 1; }
[ "$(blob $WTSM/d18_secant.py | cut -c1-8)" = eb1396ad ] && [ "$(blob $IN/d18_secant.py | cut -c1-8)" = eb1396ad ] || { step "SCAN STOP: d18_secant.py is not blob eb1396ad"; exit 1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WTS diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { step "SCAN STOP: $f.py of the scanner worktree differs from 505d8399"; exit 1; }; done
[ -z "$(git -C $WTS status --short solver | grep -v 'solver/matter/data/')" ] || { step "SCAN STOP: the scanner worktree solver/ has changes"; exit 1; }
[ "$MODE" = dry ] && { n=0; for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; n=$((n + $(echo ${LAMP[$p]} | tr ',' '\n' | wc -l))); done; echo "dry run: pins ok, $n evaluations"; exit 0; }
SB=$(blob $STATE | cut -c1-8); RB=$(blob $STUB | cut -c1-8)
cd $WTSM
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest > $OUT/selftest_secant.txt 2>&1; q0=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftest_secant_half.txt 2>&1; q1=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftest_secant_norobust.txt 2>&1; q2=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftest_secant_nosigncheck.txt 2>&1; q3=$?
step "d18_secant.py (92b9bf53, blob eb1396ad) selftest exit $q0 (0 wanted); --mutate=half exit $q1, norobust exit $q2, nosigncheck exit $q3 (1 wanted each)"
[ $q0 = 0 ] && [ $q1 = 1 ] && [ $q2 = 1 ] && [ $q3 = 1 ] || { step "SCAN STOP: the scanner's selftest or a control did not read as written"; exit 1; }
cd $OUT
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_secant.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples.csv; done ) &
SAMP=$!
step "scan starts: D $D, $NEVAL evaluations (window $WIN1, repeat of $REP), $NP procs x 1 thread, nice 10; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8); --pin=$SB,$RB"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTSM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 \
      /usr/bin/time -v $PY -u $WTSM/d18_secant.py scan $STUB $STATE $D "$mine" $SCAN/scan_D${D}_p$p.jsonl --pin=$SB,$RB > $SCAN/scan_p$p.raw 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
kill $SAMP $MEM 2>/dev/null
cat $SCAN/scan_D${D}_p*.jsonl > $OUT/merged_D${D}.jsonl
python3 -I -c "
import json
rows = sorted((json.loads(l) for l in open('$OUT/merged_D${D}.jsonl') if l.strip()), key=lambda r: r['lam'])
print(len(rows), 'evaluations', sum(r['noise_robust'] for r in rows), 'noise-robust')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.raw | sort | uniq -c >> $OUT/steps.txt
grep -hE 'Elapsed|Maximum resident' $SCAN/scan_p*.raw | sort | uniq -c >> $OUT/steps.txt
cd $IN
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
{ echo "== window: read_lower.py scan $WIN1 (a contiguous 0.02 grid)"; $PY -I read_lower.py $SCAN $WIN1; echo "(exit $?)"; } > $OUT/read_lower.txt 2>&1
step "read_lower.py read the window (reading in read_lower.txt)"
$PY -I repeat_check.py $OUT/merged_D${D}.jsonl >> $OUT/read_lower.txt 2>&1; step "repeat_check.py exit $?"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
