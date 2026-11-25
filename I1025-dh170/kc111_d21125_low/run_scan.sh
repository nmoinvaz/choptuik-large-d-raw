#!/bin/bash
# #1025 kc111_d21125_low (t5's order, 25 Nov): hybrid sign scan of the same accepted k_c 111 state at D 21.125, LOW side: lambda 0.840, 0.850, 0.860, 0.865 and a repeat of 0.860 (5 evaluations), d18_hybsign.py
# (e089207a, unmodified), 5 single-thread processes at nice 10, one round (the lists of stage.conf). Memory: alert only, nothing killed on memory. Then read_lower.py selftest (0), its mutations shift and round2 (1 each),
# the reader on the low window (the new points with the parent's 0.870) and on the whole 0.840-0.910 (the parent's nine points in prev/), repeat_check.py. Starts only after VERDICT_parent.txt says ACCEPTED and the state and record are the pinned blobs. usage: run_scan.sh [dry]. A systemd user unit.
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc111_d21125_low
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
grep -q '^ACCEPTED' $OUT/VERDICT_parent.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED parent verdict"; exit 1; }
while read -r h f; do [ "$(blob $IN/$f)" = "$h" ] || { step "SCAN STOP: in/$f is not blob $h"; exit 1; }; done < $OUT/in_blobs.txt
while read -r h f; do [ "$(blob $OUT/prev/$f)" = "$h" ] || { step "SCAN STOP: prev/$f is not blob $h"; exit 1; }; done < $OUT/prev_blobs.txt
STATE=$OUT/sol_${TAG}_${DT}.npy; STUB=$OUT/$TAG.jsonl
[ "$(blob $STATE | cut -c1-8)" = $STATE_BLOB ] && [ "$(blob $STUB | cut -c1-8)" = $REC_BLOB ] || { step "SCAN STOP: the state or record is not $STATE_BLOB / $REC_BLOB"; exit 1; }
[ -s $STATE ] && [ -s $STUB ] && [ -s $WTM/data/sol_${TAG}_${DT}.npy ] && [ -s $WTM/data/$TAG.jsonl ] || { step "SCAN STOP: the accepted state or record is missing or empty"; exit 1; }
[ "$(blob $STATE)" = "$(blob $WTM/data/sol_${TAG}_${DT}.npy)" ] && [ "$(blob $STUB)" = "$(blob $WTM/data/$TAG.jsonl)" ] || { step "SCAN STOP: the accepted state or record differs from the worktree's"; exit 1; }
[ -e $SCAN ] && [ "$MODE" != dry ] && { step "SCAN STOP: $SCAN exists"; exit 1; }
NP=${#LAMP[@]}
[ "$MODE" = dry ] && { n=0; for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; n=$((n + $(echo ${LAMP[$p]} | tr ',' '\n' | wc -l))); done; echo "dry run: pins ok, $n evaluations"; exit 0; }
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_hybsign.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples.csv; done ) &
SAMP=$!
step "scan starts: D $D, $NEVAL evaluations (window $WIN1, repeat of $REP), $NP procs x 1 thread, nice 10; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      /usr/bin/time -v $PY -u $IN/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D${D}low_p$p.jsonl > $SCAN/scanlow_p$p.raw 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
kill $SAMP $MEM 2>/dev/null
cat $SCAN/scan_D${D}low_p*.jsonl > $OUT/merged_low_D${D}.jsonl
python3 -I -c "
import json
rows = sorted((json.loads(l) for l in open('$OUT/merged_low_D${D}.jsonl') if l.strip()), key=lambda r: r['lam'])
print(len(rows), 'evaluations', sum(r['noise_robust'] for r in rows), 'noise-robust')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scanlow_p*.raw | sort | uniq -c >> $OUT/steps.txt
grep -hE 'Elapsed|Maximum resident' $SCAN/scanlow_p*.raw | sort | uniq -c >> $OUT/steps.txt
cd $IN
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
mkdir -p $OUT/combined; cp $SCAN/scan_D${D}low_p*.jsonl $OUT/combined/; cp $OUT/prev/scan_*.jsonl $OUT/combined/
cat $OUT/combined/scan_*_p*.jsonl > $OUT/merged_all_D${D}.jsonl
{ echo "== low window: read_lower.py combined $WIN1 (the new points and the parent's 0.870)"; $PY -I read_lower.py $OUT/combined $WIN1; echo "(exit $?)"
  echo; echo "== whole range: read_lower.py combined $WIN2 (the new points and the parent's nine)"; $PY -I read_lower.py $OUT/combined $WIN2; echo "(exit $?)"; } > $OUT/read_lower.txt 2>&1
step "read_lower.py read both windows (reading in read_lower.txt)"
$PY -I repeat_check.py $OUT/merged_low_D${D}.jsonl >> $OUT/read_lower.txt 2>&1; step "repeat_check.py exit $?"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
