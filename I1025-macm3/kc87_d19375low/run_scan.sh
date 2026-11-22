#!/bin/bash
# #1025 macm3b kc87_d19375low (t5's hc 2026-11-22 ~22:45 UTC): hybrid sign scan of the same accepted k_c 87 D 19.375 state as ../kc87_d19375/, lambda 1.28 to 1.40 at 0.01 (13 values)
# plus a repeat of 1.34 (on another process than the first 1.34), 4 processes of 1 thread, nice 10, own session under caffeinate -is, with d18_hybsign.py (e089207a, unmodified),
# then dh170's read_lower.py (89309d3c) with its selftest and mutations. The state and the record are pinned from raw f7862ac2 and checked again by kc87_syscheck_1025.py (6df5d960).
# Free memory: at least 12 GiB at the start (the k_c 87 scan of 1.40 to 1.50 peaked at 11.22 GB for the four); sampled every 60 s (log only). No hc from here.
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d19375low
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc87macm3d19375; D=19.375
SCAN=$OUT/scan; mkdir -p $SCAN
STATE=$WTM/data/sol_${TAG}_D19.3750.npy; STUB=$WTM/data/$TAG.jsonl
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "SCAN STOP: $*"; exit 1; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
chk() { [ "$(blob $OUT/in/$1)" = "$2" ] || stop "in/$1 is not blob $2"; }
chk sol_l1kc87macm3d19375_D19.3750.npy 448970da; chk l1kc87macm3d19375.jsonl f399e0f2; chk kc87_syscheck_1025.py 6df5d960
chk d18_hybsign.py e089207a; chk read_lower.py 89309d3c; chk d185_scan_read.py 7c9d400f
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ "$(git hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
# the worktree's copies of the state and the record are the pinned bytes (copied from in/ if they differ)
for f in sol_${TAG}_D19.3750.npy $TAG.jsonl; do
  [ "$(blob $WTM/data/$f)" = "$(blob $OUT/in/$f)" ] 2>/dev/null || cp $OUT/in/$f $WTM/data/$f
done
[ "$(blob $STATE)" = 448970da ] && [ "$(blob $STUB)" = f399e0f2 ] || stop "the worktree's state or record is not the pinned blob"
step "pins ok: state 448970da and record f399e0f2 (raw f7862ac2), kc87_syscheck 6df5d960, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f; worktree 505d8399; state and record in $WTM/data are the pinned bytes"
# the same state is accepted again on this build: dh610's k_c 87 check with its selftest and both controls
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r0=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "kc87_syscheck_1025.py: selftest exit $r0, state check exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
[ $r0 = 0 ] && [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] || stop "the check or a control did not read as written"
echo "ACCEPTED $(stamp) UTC (the pinned state of ../kc87_d19375/, accepted there; checked again here)" > $OUT/VERDICT.txt
NP=4
AVAIL=$(availgib)
step "memory before the scan: about $AVAIL GiB available (free+inactive+speculative+purgeable), $(memory_pressure | tail -1 | sed 's/.*: //') free by memory_pressure; the k_c 87 scan of 1.40 to 1.50 peaked at 11.22 GB for $NP processes (2.77 to 3.59 GB each)"
python3 -c "import sys; sys.exit(0 if $AVAIL >= 12 else 1)" || stop "less than 12 GiB available"
LAMS=()
while read -r v; do LAMS+=("$v"); done < <(python3 -I -c "
print(*[f'{v/100:.2f}' for v in range(128, 141)] + ['1.34'], sep='\n')")
step "scan starts: D $D, ${#LAMS[@]} values (1.28 to 1.40 and the repeat of 1.34), $NP procs x 1 thread, nice 10; state sol_${TAG}_D19.3750.npy $(blob $STATE), record $(blob $STUB)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LAMS[@]}; i += NP)); do mine="$mine,${LAMS[$i]}"; done; mine=${mine#,}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1 \
      $PY -u $OUT/capped_run.py 28800 $PY -u $OUT/in/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D19.375_p$p.jsonl > $SCAN/scan_p$p.log 2>&1
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
cat $SCAN/scan_D19.375_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$SCAN/scan_D19.375_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $SCAN/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $OUT/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
$PY -I read_lower.py $SCAN 1.28 1.40 > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
# the point 1.40 was also evaluated in ../kc87_d19375/ (process 0 there): information
python3 -I - > $OUT/cross_run_1.40.txt 2>&1 <<PYEOF
import json
a=[json.loads(l) for l in open('$OUT/../kc87_d19375/scan/scan_D19.375_1025.jsonl') if abs(json.loads(l)['lam']-1.40)<1e-9]
b=[json.loads(l) for l in open('$SCAN/scan_D19.375_1025.jsonl') if abs(json.loads(l)['lam']-1.40)<1e-9]
print('1.40 in kc87_d19375:', [(r['sign'], r['ln'], r['noise'], r['f64_sign']) for r in a])
print('1.40 here          :', [(r['sign'], r['ln'], r['noise'], r['f64_sign']) for r in b])
print('agree (sign, noise, float64 sign, ln within 1e-6):', bool(a and b and a[0]['sign']==b[0]['sign'] and a[0]['noise']==b[0]['noise'] and a[0]['f64_sign']==b[0]['f64_sign'] and abs(a[0]['ln']-b[0]['ln'])<1e-6))
PYEOF
step "cross-run check of lambda 1.40 against ../kc87_d19375/: $(tail -1 $OUT/cross_run_1.40.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
