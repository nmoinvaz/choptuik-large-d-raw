#!/bin/bash
# #1025 kc119_d2225 EXTENSION (t5's hc, 27 Nov 02:11 UTC, to start after the repeat of 0.04 has landed): the same scan as run_scan.sh (d18_secant.py scan, worktree -1025sp at 92b9bf53, blob eb1396ad, --pin the regrid result's blobs),
# widened downward only: lambda -0.06, -0.08, -0.10 (3 evaluations), 3 single-thread processes at nice 19 (t5), after the same memory gate (MemAvailable of at least 19000 MiB, at most 6 h), the scanner's selftests again, then read_lower.py on the extension window
# -0.10 to -0.04 and on the whole -0.10 to 0.12 (the original nine points and the extension: a contiguous 0.02 grid), repeat_check.py on all of it. Starts only after SCAN_DONE.txt exists (the original scan, repeat of 0.04 included, has ended).
# This is run_scan.sh with the lists, the nice value, the output names and the reading changed (run_scan_ext_vs_run_scan.diff). usage: run_scan_ext.sh [dry]. Run by ext_after_scan.sh in a systemd user unit.
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
[ -e $SCAN/scan_D${D}e_p0.jsonl ] && [ "$MODE" != dry ] && { step "EXT STOP: the extension has already run"; exit 1; }
[ -e $OUT/SCAN_DONE.txt ] || [ "$MODE" = dry ] || { step "EXT STOP: the scan has not finished (no SCAN_DONE.txt)"; exit 1; }
LAMP=("${LAMPE[@]}"); NP=${#LAMP[@]}
# the new scanner: worktree -1025sp at 92b9bf53, d18_secant.py blob eb1396ad (= in/d18_secant.py), dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399
[ "$(git -C $WTS rev-parse --short=8 HEAD)" = 92b9bf53 ] || { step "SCAN STOP: the scanner worktree is not at 92b9bf53"; exit 1; }
[ "$(blob $WTSM/d18_secant.py | cut -c1-8)" = eb1396ad ] && [ "$(blob $IN/d18_secant.py | cut -c1-8)" = eb1396ad ] || { step "SCAN STOP: d18_secant.py is not blob eb1396ad"; exit 1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WTS diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { step "SCAN STOP: $f.py of the scanner worktree differs from 505d8399"; exit 1; }; done
[ -z "$(git -C $WTS status --short solver | grep -v 'solver/matter/data/')" ] || { step "SCAN STOP: the scanner worktree solver/ has changes"; exit 1; }
[ "$MODE" = dry ] && { n=0; for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; n=$((n + $(echo ${LAMP[$p]} | tr ',' '\n' | wc -l))); done; echo "dry run: pins ok, $n evaluations"; exit 0; }
SB=$(blob $STATE | cut -c1-8); RB=$(blob $STUB | cut -c1-8)
t0=$(date +%s)
while true; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  [ "$av" -ge 19000 ] && break
  [ $(( $(date +%s) - t0 )) -ge 21600 ] && { step "EXT STOP: MemAvailable stayed under 19000 MiB for 6 h (now $av): no extension"; exit 1; }
  [ -e $OUT/gate_ext_waiting ] || { step "extension gate: MemAvailable $av MiB is under 19000; waiting (up to 6 h)"; echo $av > $OUT/gate_ext_waiting; }
  sleep 60
done
step "extension gate passed: MemAvailable $av MiB (waited $(( $(date +%s) - t0 )) s)"
cd $WTSM
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest > $OUT/selftest_secant_ext.txt 2>&1; q0=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftest_secant_half_ext.txt 2>&1; q1=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftest_secant_norobust_ext.txt 2>&1; q2=$?
nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftest_secant_nosigncheck_ext.txt 2>&1; q3=$?
step "EXTENSION: d18_secant.py (92b9bf53, blob eb1396ad) selftest exit $q0 (0 wanted); --mutate=half exit $q1, norobust exit $q2, nosigncheck exit $q3 (1 wanted each)"
[ $q0 = 0 ] && [ $q1 = 1 ] && [ $q2 = 1 ] && [ $q3 = 1 ] || { step "SCAN STOP: the scanner's selftest or a control did not read as written"; exit 1; }
cd $OUT
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_secant.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples_ext.csv; done ) &
SAMP=$!
step "EXTENSION scan starts: D $D, $NEVALE evaluations (lambda ${LAMPE[*]}, window $WINE), $NP procs x 1 thread, nice 19; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8); --pin=$SB,$RB"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTSM && nice -n 19 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 \
      /usr/bin/time -v $PY -u $WTSM/d18_secant.py scan $STUB $STATE $D "$mine" $SCAN/scan_D${D}e_p$p.jsonl --pin=$SB,$RB > $SCAN/scan_e_p$p.raw 2>&1
    rc=$?; echo "$(stamp) UTC EXT proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
kill $SAMP $MEM 2>/dev/null
cat $SCAN/scan_D${D}e_p*.jsonl > $OUT/merged_ext_D${D}.jsonl
cat $SCAN/scan_D${D}_p*.jsonl $SCAN/scan_D${D}e_p*.jsonl > $OUT/merged_all_D${D}.jsonl
python3 -I -c "
import json
rows = sorted((json.loads(l) for l in open('$OUT/merged_ext_D${D}.jsonl') if l.strip()), key=lambda r: r['lam'])
print('EXT', len(rows), 'evaluations', sum(r['noise_robust'] for r in rows), 'noise-robust')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_e_p*.raw | sort | uniq -c >> $OUT/steps.txt
grep -hE 'Elapsed|Maximum resident' $SCAN/scan_e_p*.raw | sort | uniq -c >> $OUT/steps.txt
cd $IN
$PY -I read_lower.py selftest > $OUT/selftest_read_lower_ext.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift_ext.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2_ext.txt 2>&1; e2=$?
step "EXT read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
{ echo "== extension window: read_lower.py scan $WINE (the extension and the original -0.04)"; $PY -I read_lower.py $SCAN $WINE; echo "(exit $?)"
  echo; echo "== whole window: read_lower.py scan $WINALL (the original nine and the extension: a contiguous 0.02 grid)"; $PY -I read_lower.py $SCAN $WINALL; echo "(exit $?)"; } > $OUT/read_lower_ext.txt 2>&1
step "EXT read_lower.py read the windows (reading in read_lower_ext.txt)"
$PY -I repeat_check.py $OUT/merged_all_D${D}.jsonl >> $OUT/read_lower_ext.txt 2>&1; step "EXT repeat_check.py exit $?"
echo "SCAN EXT DONE $(stamp) UTC" > $OUT/SCAN_EXT_DONE.txt
step "extension done"
exit 0
}
