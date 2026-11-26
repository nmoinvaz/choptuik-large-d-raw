#!/bin/bash
# #1025 kc119_d230625 step 4 (t5's order and its change of 06:14 UTC): hybrid sign scan of the accepted k_c 119 state at D 23.0625, lambda -0.04 to 0.04 by 0.02 (5 values, no repeat), d18_hybsign.py (e089207a,
# unmodified), in rounds of at most 3 single-thread processes at nice 10 (3 then 2; the lists of stage.conf). Memory: alert only. Then read_lower.py selftest (0), its mutations shift and round2 (1 each) and the
# reader on the window. Starts only after VERDICT.txt says ACCEPTED. usage: run_scan.sh [dry]. A systemd user unit (lane_k119.sh).
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc119_d230625
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
step "scan starts: D $D, $NEVAL evaluations (window $WIN1, no repeat), $NP procs x 1 thread, nice 10; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8)"
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
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
