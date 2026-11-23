#!/bin/bash
# #1025 kc87_d1975 step 2 (t5's order): hybrid sign scan of the accepted k_c 87 D 19.75 state, lambda 1.30 to 1.36 at 0.01 (7 values) plus a repeat of 1.33, 4 processes of 1 thread at nice 10, d18_hybsign.py (e089207a,
# unmodified): p0 1.30,1.34; p1 1.31,1.35; p2 1.32,1.36; p3 1.33,1.33 (the order's split: the repeat runs on the same process as the first 1.33). Memory: alert only. Then read_lower.py selftest (0), its mutations shift and
# round2 (1 each), the reader and repeat_check.py. Starts only after VERDICT.txt says ACCEPTED. usage: run_scan.sh [dry]. A systemd user unit (i1025-k87s).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc87_d1975
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc87dh170d1975; D=19.75
SCAN=$OUT/scan
MODE=${1:-}
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1"; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
while read -r h f; do [ "$(blob $OUT/in/$f)" = "$h" ] || { step "SCAN STOP: in/$f is not blob $h"; exit 1; }; done < $OUT/in_blobs.txt
STATE=$OUT/sol_${TAG}_D19.7500.npy; STUB=$OUT/$TAG.jsonl
[ "$(blob $STATE)" = "$(blob $WTM/data/sol_${TAG}_D19.7500.npy)" ] && [ "$(blob $STUB)" = "$(blob $WTM/data/$TAG.jsonl)" ] || { step "SCAN STOP: the accepted state or record differs from the worktree's"; exit 1; }
[ -e $SCAN ] && [ "$MODE" != dry ] && { step "SCAN STOP: $SCAN exists"; exit 1; }
LAMP=("1.30,1.34" "1.31,1.35" "1.32,1.36" "1.33,1.33"); NP=4
[ "$MODE" = dry ] && { for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; done; echo "dry run: pins ok, 8 evaluations"; exit 0; }
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_hybsign.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples.csv; done ) &
SAMP=$!
step "scan starts: D $D, 8 evaluations (1.30 to 1.36 and the repeat of 1.33), $NP procs x 1 thread, nice 10; state sol_${TAG}_D19.7500.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      /usr/bin/time -v $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D19.75_p$p.jsonl > $SCAN/scan_p$p.raw 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
kill $SAMP $MEM 2>/dev/null
cat $SCAN/scan_D19.75_p*.jsonl > $OUT/merged_D19.75.jsonl
python3 -I -c "
import json
rows = sorted((json.loads(l) for l in open('$OUT/merged_D19.75.jsonl') if l.strip()), key=lambda r: r['lam'])
print(len(rows), 'evaluations', sum(r['noise_robust'] for r in rows), 'noise-robust')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.raw | sort | uniq -c >> $OUT/steps.txt
grep -hE 'Elapsed|Maximum resident' $SCAN/scan_p*.raw | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 1.30 1.36 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
$PY -I repeat_check.py $OUT/merged_D19.75.jsonl >> $OUT/read_lower.txt 2>&1; step "repeat_check.py exit $?"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
