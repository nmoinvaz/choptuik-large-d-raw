#!/bin/bash
# #1025 kc79_d19125 step 2 (t5's order): hybrid sign scan of the accepted k_c 79 D 19.125 state, lambda 1.44 to 1.58 at 0.01 (15 values) plus a
# repeat of 1.50 (on another process than the first 1.50), 6 processes of 1 thread, nice 10, with d18_hybsign.py (e089207a, unmodified), then dh170's
# read_lower.py (89309d3c) and its selftest and mutations. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc79_d19125
WT=/home/nathan/Source/choptuik-large-d-1025; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc79dh370; D=19.125
SCAN=$OUT/scan; mkdir -p $SCAN
STATE=$WTM/data/sol_${TAG}_D19.1250.npy; STUB=$WTM/data/$TAG.jsonl
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
[ "$(blob $OUT/in/d18_hybsign.py)" = e089207a ] || { step "SCAN STOP: d18_hybsign.py is not e089207a"; exit 1; }
[ "$(blob $OUT/in/read_lower.py)" = 89309d3c ] || { step "SCAN STOP: read_lower.py is not 89309d3c"; exit 1; }
cp $STATE $STUB $OUT/in/
mapfile -t LAMS < <(python3 -I -c "
print(*[f'{v/100:.2f}' for v in range(144, 159)] + ['1.50'], sep='\n')")
NP=6
step "scan starts: D $D, ${#LAMS[@]} values (1.44 to 1.58 and the repeat of 1.50), $NP procs x 1 thread, nice 10; state sol_${TAG}_D19.1250.npy $(blob $STATE), record $(blob $STUB)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LAMS[@]}; i += NP)); do mine="$mine,${LAMS[$i]}"; done; mine=${mine#,}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D19.125_p$p.jsonl > $SCAN/scan_p$p.log 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
cat $SCAN/scan_D19.125_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$SCAN/scan_D19.125_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 1.44 1.58 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
