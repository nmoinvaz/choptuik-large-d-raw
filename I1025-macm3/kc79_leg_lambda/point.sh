#!/bin/bash
# #1025 macm3b kc79_leg_lambda (t5's rolling order, hc 2026-11-23 ~15:28 UTC): lambda_1 at one point D of win2's k_c 79 leg (raw I1025-win2/kc79_leap/states/, tag l1kc79Lw1025d), no regrid.
# usage: bash point.sh DNAME   (DNAME/point.env: D DNAME TAG RAWC STATEFILE STATEBLOB RECBLOB LO HI REPEAT; LO and HI in hundredths of lambda)
# steps: (0) copy the state and the record from the raw commit RAWC with git cat-file and check their blobs; (1) kc79_syscheck_1025.py selftest, the check and both controls (kc79_syscheck must accept, both controls exit 1);
# (2) d18_hybsign.py (e089207a, unmodified) at LO..HI by 0.01 plus one repeat (on another process than the first), 4 processes of 1 thread, nice 10, each under capped_run.py 28800 by exact pid, at least 8 GiB available at the start;
# (3) read_lower.py selftest, its mutations shift and round2, and read_lower.py SCAN LO HI. Steps and the verdict go to DNAME/steps.txt and VERDICT.txt; no hc from here. Own session under caffeinate -is. Stops at the first failure.
{
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_leg_lambda
DN=$1; OUT=$L/$DN
. $OUT/point.env
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
cd $OUT || exit 9
mkdir -p $OUT/in $OUT/scan
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
chkc() { [ "$(blob $L/common/in/$1)" = "$2" ] || stop "common/in/$1 is not blob $2"; }
step "start D $D (loadavg $(sysctl -n vm.loadavg), free memory $(memory_pressure | tail -1 | sed 's/.*: //'), disk $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}') free)"
chkc kc79_syscheck_1025.py 29dce7ea; chkc d18_hybsign.py e089207a; chkc read_lower.py 89309d3c; chkc d185_scan_read.py 7c9d400f
git -C $RAWG cat-file blob $RAWC:I1025-win2/kc79_leap/states/$STATEFILE > $OUT/in/$STATEFILE || stop "cannot read the state at $RAWC"
git -C $RAWG cat-file blob $RAWC:I1025-win2/kc79_leap/states/$TAG.jsonl > $OUT/in/$TAG.jsonl || stop "cannot read the record at $RAWC"
[ "$(blob $OUT/in/$STATEFILE)" = "$STATEBLOB" ] || stop "state blob $(blob $OUT/in/$STATEFILE), wanted $STATEBLOB"
[ "$(blob $OUT/in/$TAG.jsonl)" = "$RECBLOB" ] || stop "record blob $(blob $OUT/in/$TAG.jsonl), wanted $RECBLOB"
{ echo "$STATEBLOB  $STATEFILE  <- $RAWC:I1025-win2/kc79_leap/states/$STATEFILE  ok"; echo "$RECBLOB  $TAG.jsonl  <- $RAWC:I1025-win2/kc79_leap/states/$TAG.jsonl  ok"; } > $OUT/pins.txt
step "inputs pinned: state $STATEBLOB and record $RECBLOB from raw $RAWC; kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f (common/in/)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 505d8399, clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
STATE=$WTM/data/$STATEFILE; STUB=$WTM/data/${TAG}_asof_D$D.jsonl
[ ! -e $STATE ] && [ ! -e $STUB ] || stop "data/ already holds $STATEFILE or $STUB"
cp $OUT/in/$STATEFILE $STATE; cp $OUT/in/$TAG.jsonl $STUB
[ "$(blob $STATE)" = "$STATEBLOB" ] && [ "$(blob $STUB)" = "$RECBLOB" ] || stop "copied blobs differ"
nice -n 10 $PY -I $L/common/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
step "selftest: kc79_syscheck exit $r1 (0 wanted)"; [ $r1 = 0 ] || stop "the selftest failed"
nice -n 10 $PY -I $L/common/in/kc79_syscheck_1025.py $STUB $STATE $D $WTM > $OUT/syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $L/common/in/kc79_syscheck_1025.py $STUB $STATE $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $L/common/in/kc79_syscheck_1025.py $STUB $STATE $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; s2=$?
step "source check (kc79_syscheck_1025.py on win2's k_c 79 D $D state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each): $(tail -2 $OUT/syscheck.txt | head -1 | cut -c1-220)"
if [ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else stop "the source check or a control did not read as written (exit $s0, $s1, $s2)"; fi
step "verdict: ACCEPTED"
NP=${NP:-4}
AVAIL=$(availgib)
step "memory before the scan: about $AVAIL GiB available (free+inactive+speculative+purgeable), $(memory_pressure | tail -1 | sed 's/.*: //') free by memory_pressure; $NP processes of about 1.3 to 4 GB each (D 20.78125: largest child 3.99 GB)"
python3 -c "import sys; sys.exit(0 if $AVAIL >= 8 else 1)" || stop "less than 8 GiB available"
# the values: LO..HI by 0.01, then the repeat on another process than the first one (round-robin by index; the repeat goes to the next process)
BASE=(); for ((v = LO; v <= HI; v++)); do BASE+=("$(python3 -c "print('%.2f' % ($v / 100))")"); done
first=-1; for ((i = 0; i < ${#BASE[@]}; i++)); do [ "${BASE[$i]}" = "$REPEAT" ] && { first=$i; break; }; done
[ $first -ge 0 ] || stop "the repeat $REPEAT is not among the values"
RP=$(( (first % NP + 1) % NP ))
step "scan starts: D $D, ${#BASE[@]} values ($(printf '%.2f' $(python3 -c "print($LO/100)")) to $(printf '%.2f' $(python3 -c "print($HI/100)"))) and the repeat of $REPEAT on process $RP (the first $REPEAT on process $((first % NP))), $NP procs x 1 thread, nice 10; state $STATEFILE $(blob $STATE), record $(blob $STUB)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#BASE[@]}; i += NP)); do mine="$mine,${BASE[$i]}"; done
  [ $p = $RP ] && mine="$mine,$REPEAT"
  mine=${mine#,}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1 \
      $PY -u $L/common/capped_run.py 28800 $PY -u $L/common/in/d18_hybsign.py $STUB $STATE $D "$mine" $OUT/scan/scan_D${D}_p$p.jsonl > $OUT/scan/scan_p$p.log 2>&1
    rc=$?; echo "$(stamp) UTC proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
  sleep 2
  step "proc $p lambda $mine: capped_run $(grep -o 'child pid [0-9]*' $OUT/scan/scan_p$p.log | head -1) (cap 28800 s)"
done
echo "time_utc,pid,rss_kB,pcpu,avail_GiB,free_mem_pct,free_disk" > $OUT/scan/scan_samples.csv
( while :; do
    alive=0; for q in "${pids[@]}"; do kill -0 $q 2>/dev/null && alive=1; done
    [ $alive = 0 ] && break
    m=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//'); dk=$(df -h /System/Volumes/Data | tail -1 | awk '{print $4}'); t=$(stamp); av=$(availgib)
    for c in $(grep -ho 'child pid [0-9]*' $OUT/scan/scan_p*.log | awk '{print $3}'); do
      ps -o rss=,pcpu= -p $c 2>/dev/null | awk -v t="$t" -v c=$c -v m="$m" -v dk="$dk" -v av="$av" '{print t","c","$1","$2","av","m","dk}' >> $OUT/scan/scan_samples.csv
    done
    sleep 60
  done ) &
wait "${pids[@]}"
cat $OUT/scan/scan_D${D}_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$OUT/scan/scan_D${D}_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'points')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $OUT/scan/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $L/common/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
LOF=$(python3 -c "print('%.2f' % ($LO / 100))"); HIF=$(python3 -c "print('%.2f' % ($HI / 100))")
$PY -I read_lower.py $OUT/scan $LOF $HIF > $OUT/read_lower.txt 2>&1; step "read_lower.py exit $? (reading in read_lower.txt)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
