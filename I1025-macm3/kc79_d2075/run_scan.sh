#!/bin/bash
# #1025 macm3b kc79_d2075 step 3 (t5's order): hybrid sign scan of win2's accepted k_c 79 D 20.75 state (no regrid), lambda 0.95 to 1.07 at 0.01 (13 values) plus a repeat of 1.01
# (on another process than the first 1.01), 4 processes of 1 thread, nice 10, own session under caffeinate -is, with d18_hybsign.py (e089207a, unmodified), then dh170's
# read_lower.py (89309d3c) with its selftest and mutations. Only after VERDICT.txt reads ACCEPTED (run_source.sh). At least 8 GiB available at the start
# (4 processes x about 1.3 GB at k_c 79); sampled every 60 s (log only). No hc from here.
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d2075
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc79win2d2075; D=20.75
SCAN=$OUT/scan; mkdir -p $SCAN
STATE=$WTM/data/sol_${TAG}_D20.7500.npy; STUB=$WTM/data/$TAG.jsonl
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "SCAN STOP: $*"; exit 1; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
chk() { [ "$(blob $OUT/in/$1)" = "$2" ] || stop "in/$1 is not blob $2"; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
chk d18_hybsign.py e089207a; chk read_lower.py 89309d3c; chk d185_scan_read.py 7c9d400f
NP=4
AVAIL=$(availgib)
step "memory before the scan: about $AVAIL GiB available (free+inactive+speculative+purgeable), $(memory_pressure | tail -1 | sed 's/.*: //') free by memory_pressure; 4 processes x about 1.3 GB at k_c 79"
python3 -c "import sys; sys.exit(0 if $AVAIL >= 8 else 1)" || stop "less than 8 GiB available"
LAMS=()
while read -r v; do LAMS+=("$v"); done < <(python3 -I -c "
print(*[f'{v/100:.2f}' for v in range(95, 107)] + ['1.07', '1.01'], sep='\n')")
step "scan starts: D $D, ${#LAMS[@]} values (0.95 to 1.07 and the repeat of 1.01), $NP procs x 1 thread, nice 10; state sol_${TAG}_D20.7500.npy $(blob $STATE), record $(blob $STUB)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LAMS[@]}; i += NP)); do mine="$mine,${LAMS[$i]}"; done; mine=${mine#,}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1 \
      $PY -u $OUT/capped_run.py 28800 $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D20.75_p$p.jsonl > $SCAN/scan_p$p.log 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
  sleep 2
  step "proc $p lambda $mine: capped_run $(grep -o 'child pid [0-9]*' $SCAN/scan_p$p.log | head -1) (cap 28800 s)"
done
# resource sampler (log only, never stops or kills anything): rss and cpu of each scan child, available memory (GiB, vm_stat), free memory percent, free disk
echo "time_utc,pid,rss_kB,pcpu,avail_GiB,free_mem_pct,free_disk" > $SCAN/scan_samples.csv
( while :; do
    alive=0; for q in "${pids[@]}"; do kill -0 $q 2>/dev/null && alive=1; done
    [ $alive = 0 ] && break
    m=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//'); dk=$(df -h /System/Volumes/Data | tail -1 | awk '{print $4}'); t=$(stamp); av=$(availgib)
    for c in $(grep -ho 'child pid [0-9]*' $SCAN/scan_p*.log | awk '{print $3}'); do
      ps -o rss=,pcpu= -p $c 2>/dev/null | awk -v t="$t" -v c=$c -v m="$m" -v dk="$dk" -v av="$av" '{print t","c","$1","$2","av","m","dk}' >> $SCAN/scan_samples.csv
    done
    sleep 60
  done ) &
wait "${pids[@]}"
cat $SCAN/scan_D20.75_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$SCAN/scan_D20.75_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 0.95 1.07 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
