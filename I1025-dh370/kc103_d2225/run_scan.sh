#!/bin/bash
# #1025 kc103_d21125 step 3 (t5's order): hybrid sign scan of the accepted k_c 103 state at D 21.125, lambda 0.875 to 0.895 at 0.005 (5 values) and a repeat of 0.885 (6 evaluations), d18_hybsign.py (e089207a, unmodified), 4
# single-thread processes at nice 10 (the lists of stage.conf: round 1 the four points nearest the prediction, round 2 two). Memory: alert only. Then read_lower.py selftest (0), its mutations shift and round2 (1 each), the reader on the
# window and repeat_check.py. Starts only after VERDICT.txt says ACCEPTED. usage: run_scan.sh [dry]. A systemd user unit.
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc103_d2225
MODE=${1:-}
OUT=$ROOT; IN=$OUT/in
WT=/home/nathan/Source/choptuik-large-d-1025; WTM=$WT/solver/matter
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
[ "$MODE" = dry ] && { n=0; for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; n=$((n + $(echo ${LAMP[$p]} | tr ',' '\n' | wc -l))); done; echo "dry run: pins ok, $n evaluations"; exit 0; }
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 1024 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_hybsign.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples.csv; done ) &
SAMP=$!
step "scan starts: D $D, $NEVAL evaluations (window $WIN1, repeat of $REP), $NP procs x 1 thread, nice 10; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      /usr/bin/time -v $PY -u $IN/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D${D}_p$p.jsonl > $SCAN/scan_p$p.raw 2>&1
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
{ echo "== window: read_lower.py scan $WIN1"; $PY -I read_lower.py $SCAN $WIN1; echo "(exit $?)"; } > $OUT/read_lower.txt 2>&1
step "read_lower.py read the window (reading in read_lower.txt)"
$PY -I repeat_check.py $OUT/merged_D${D}.jsonl >> $OUT/read_lower.txt 2>&1; step "repeat_check.py exit $?"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
