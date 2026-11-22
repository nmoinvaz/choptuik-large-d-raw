#!/bin/bash
# #1075 step 3 (t5's order): hybrid sign scan of the accepted k_c 79 D 20 state, lambda 1.22 to 1.32 at 0.01 (11 values) plus a repeat of 1.27 (on another process than the
# first 1.27), 3 processes of 1 thread, nice 10, with d18_hybsign.py (e089207a, unmodified), then dh170's read_lower.py (89309d3c), its selftest and mutations, and
# repeat_bits.py. A systemd user unit; no hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw/I1075-rpi5/kc79_d20
WT=/home/nathan/Source/choptuik-large-d-1075; WTM=$WT/solver/matter
PY=/home/nathan/Source/venv-1025/bin/python
TAG=l1kc79rpi5d20; D=20.0
SCAN=$OUT/scan; mkdir -p $SCAN
STATE=$WTM/data/sol_${TAG}_D20.0000.npy; STUB=$WTM/data/$TAG.jsonl
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
[ "$(blob $OUT/in/d18_hybsign.py)" = e089207a ] || { step "SCAN STOP: d18_hybsign.py is not e089207a"; exit 1; }
[ "$(blob $OUT/in/read_lower.py)" = 89309d3c ] || { step "SCAN STOP: read_lower.py is not 89309d3c"; exit 1; }
cp $STATE $STUB $OUT/in/
# lambda by process: the first 1.27 on p0, its repeat on p2; rounds (1.22 1.23 1.24) (1.25 1.26 1.27r) (1.27 1.28 1.29) (1.30 1.31 1.32)
LAMS=("1.22,1.25,1.27,1.30" "1.23,1.26,1.28,1.31" "1.24,1.27,1.29,1.32")
step "scan starts: D $D, 12 evaluations (1.22 to 1.32 and the repeat of 1.27), 3 procs x 1 thread, nice 10; state $(basename $STATE) $(blob $STATE), record $(blob $STUB)"
pids=()
for p in 0 1 2; do
  mine=${LAMS[$p]}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D20_p$p.jsonl > $SCAN/scan_p$p.log 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
cat $SCAN/scan_D20_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$SCAN/scan_D20_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 1.22 1.32 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
