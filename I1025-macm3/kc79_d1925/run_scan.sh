#!/bin/bash
# #1025 macm3b kc79_d1925 step 3 (t5's order): hybrid sign scan of the accepted k_c 79 D 19.25 state, lambda 1.42 to 1.52 at 0.01 (11 values) plus a repeat of 1.47
# (on another process than the first 1.47), 4 processes of 1 thread, nice 10, own session under caffeinate -is, with d18_hybsign.py (e089207a, unmodified), then dh170's
# read_lower.py (89309d3c) with its selftest and mutations. Free memory is checked first (each process about 1.3 GB). No hc from here.
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d1925
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc79macm3; D=19.25
SCAN=$OUT/scan; mkdir -p $SCAN
STATE=$WTM/data/sol_${TAG}_D19.2500.npy; STUB=$WTM/data/$TAG.jsonl
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
[ "$(blob $OUT/in/d18_hybsign.py)" = e089207a ] || { step "SCAN STOP: d18_hybsign.py is not e089207a"; exit 1; }
[ "$(blob $OUT/in/read_lower.py)" = 89309d3c ] || { step "SCAN STOP: read_lower.py is not 89309d3c"; exit 1; }
[ "$(blob $OUT/in/d185_scan_read.py)" = 7c9d400f ] || { step "SCAN STOP: d185_scan_read.py is not 7c9d400f"; exit 1; }
cp $STATE $STUB $OUT/in/
NP=4
# free memory before the scan: free + inactive + speculative + purgeable pages (16 KiB each) from vm_stat, in GiB; need NP x 1.3 GB and a margin
AVAIL=$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')
step "memory before the scan: about $AVAIL GiB available (free+inactive+speculative+purgeable), $(memory_pressure | tail -1 | sed 's/.*: //') free by memory_pressure; need $NP x 1.3 GB = $(python3 -c "print(round($NP*1.3,1))") GB"
python3 -c "import sys; sys.exit(0 if $AVAIL >= 8 else 1)" || { step "SCAN STOP: less than 8 GiB available"; exit 1; }
LAMS=()
while read -r v; do LAMS+=("$v"); done < <(python3 -I -c "
print(*[f'{v/100:.2f}' for v in range(142, 153)] + ['1.47'], sep='\n')")
step "scan starts: D $D, ${#LAMS[@]} values (1.42 to 1.52 and the repeat of 1.47), $NP procs x 1 thread, nice 10; state sol_${TAG}_D19.2500.npy $(blob $STATE), record $(blob $STUB)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LAMS[@]}; i += NP)); do mine="$mine,${LAMS[$i]}"; done; mine=${mine#,}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1 \
      $PY -u $OUT/capped_run.py 28800 $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D19.25_p$p.jsonl > $SCAN/scan_p$p.log 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
  sleep 2
  step "proc $p lambda $mine: capped_run $(grep -o 'child pid [0-9]*' $SCAN/scan_p$p.log | head -1) (cap 28800 s)"
done
wait "${pids[@]}"
cat $SCAN/scan_D19.25_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$SCAN/scan_D19.25_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 1.42 1.52 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
