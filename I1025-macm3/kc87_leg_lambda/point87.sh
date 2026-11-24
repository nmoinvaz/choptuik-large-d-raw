#!/bin/bash
# #1025 macm3 kc87_leg_lambda (t5's order, hc 2026-11-24 ~07:10 UTC): lambda_1 at one state of dh370's k_c 87 leg (raw I1025-dh370/kc87_leg/, tag l1kc87Ldh370), no regrid.
# usage: bash point87.sh DNAME accept | scan | dry      (DNAME/point.env: D TAG RAWC STATEFILE STATEBLOB RECBLOB LAMP WIN REP)
# accept: the inputs pinned by blob (prepare87.sh wrote them; checked again here), worktree 505d8399, the selftests of kc87_syscheck and kc79_syscheck (0), kc87_syscheck_1025.py on the state
#   (0), its controls --mutate=F and --mutate=steps (1 each), kc79_syscheck_1025.py on the k_c 87 state (must refuse, 1): VERDICT.txt ACCEPTED or REFUSED. No hc from here.
# scan: only after ACCEPTED: d18_hybsign.py (e089207a, unmodified) at the LAMP values, NP processes of 1 thread (default one per value; round-robin otherwise), nice 10, each under capped_run.py 28800 by exact pid, own session
#   under caffeinate -is; at least GATE GiB available at the start (12, as for the k_c 87 scan of D 19.75); every process must print `the record system`; resource sampler (log only) and an alert-only
#   watcher (hc to t5 when available memory < 2 GiB, free memory < 8% or free disk < 3 GiB; it stops and kills nothing). Then read_lower.py selftest + mutations (shift, round2), read_lower.py
#   on WIN, repeat_check.py selftest and on the merged scan. Steps go to DNAME/steps.txt.
{
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
DN=$1; MODE=${2:?accept | scan | dry}; OUT=$L/$DN
. $OUT/point.env
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
GATE=${GATE:-12}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
cd $OUT || exit 9
mkdir -p $OUT/scan
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { [ "$MODE" = accept ] && echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP ($MODE): $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
chkc() { [ "$(blob $L/common/in/$1)" = "$2" ] || stop "common/in/$1 is not blob $2"; }
step "$MODE: D $D (loadavg $(sysctl -n vm.loadavg), free memory $(memory_pressure | tail -1 | sed 's/.*: //'), $(availgib) GiB available, disk $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}') free)"
chkc kc87_syscheck_1025.py 6df5d960; chkc kc79_syscheck_1025.py 29dce7ea; chkc d18_hybsign.py e089207a; chkc read_lower.py 89309d3c; chkc d185_scan_read.py 7c9d400f; chkc repeat_check.py aaf598a9
[ "$(blob $OUT/in/$STATEFILE)" = "$STATEBLOB" ] || stop "in/$STATEFILE is not blob $STATEBLOB"
[ "$(blob $OUT/in/$TAG.jsonl)" = "$RECBLOB" ] || stop "in/$TAG.jsonl is not blob $RECBLOB"
step "inputs pinned: state $STATEBLOB and record $RECBLOB from raw $RAWC (pins.txt); kc87_syscheck 6df5d960, kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f, repeat_check aaf598a9"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 505d8399, clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
STATE=$WTM/data/$STATEFILE; STUB=$WTM/data/${TAG}_asof_D$D.jsonl
if [ "$MODE" = dry ]; then step "dry run: pins and worktree ok, nothing started; values ${LAMP[*]}"; echo "dry ok"; exit 0; fi

if [ "$MODE" = accept ]; then
  [ -e $OUT/VERDICT.txt ] && { echo "VERDICT.txt exists"; exit 2; }
  for f in $STATEFILE ${TAG}_asof_D$D.jsonl; do
    src=$OUT/in/$f; [ $f = ${TAG}_asof_D$D.jsonl ] && src=$OUT/in/$TAG.jsonl
    if [ -e $WTM/data/$f ] && [ "$(blob $WTM/data/$f)" != "$(blob $src)" ]; then stop "data/$f exists and differs from the pin"; fi
    [ -e $WTM/data/$f ] || cp $src $WTM/data/$f
    [ "$(blob $WTM/data/$f)" = "$(blob $src)" ] || stop "copied $f differs"
  done
  nice -n ${NICE:-10} $PY -I $L/common/in/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r1=$?
  nice -n ${NICE:-10} $PY -I $L/common/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r2=$?
  step "selftests: kc87_syscheck exit $r1, kc79_syscheck exit $r2 (0 wanted)"; [ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
  nice -n ${NICE:-10} $PY -I $L/common/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
  nice -n ${NICE:-10} $PY -I $L/common/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
  nice -n ${NICE:-10} $PY -I $L/common/in/kc87_syscheck_1025.py $STUB $STATE $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
  nice -n ${NICE:-10} $PY -I $L/common/in/kc79_syscheck_1025.py $STUB $STATE $D $WTM > $OUT/syscheck_kc79_refuses.txt 2>&1; a3=$?
  step "kc87_syscheck_1025.py exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc79_syscheck_1025.py on the k_c 87 state exit $a3 (1 wanted): $(grep -E '^D ' $OUT/syscheck.txt | cut -c1-260)"
  if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: kc87_syscheck $a0, controls $a1 $a2, kc79_syscheck refuses $a3" > $OUT/VERDICT.txt; fi
  step "verdict: $(cat $OUT/VERDICT.txt)"
  exit 0
fi

# MODE = scan
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
[ -e $OUT/SCAN_DONE.txt ] || [ -z "$(ls $OUT/scan 2>/dev/null)" ] || stop "scan/ is not empty"
[ "$(blob $STATE)" = "$STATEBLOB" ] && [ "$(blob $STUB)" = "$RECBLOB" ] || stop "the worktree's state or record differs from the pin"
NP=${NP:-${#LAMP[@]}}      # processes; LAMP values go round-robin to them (a process runs its values one after another)
AVAIL=$(availgib)
step "memory before the scan: about $AVAIL GiB available (free+inactive+speculative+purgeable), $(memory_pressure | tail -1 | sed 's/.*: //') free by memory_pressure; $NP processes for ${#LAMP[@]} values (the k_c 87 scan of D 19.75 with 4 processes: 4.07, 2.62, 2.52, 2.51 GB peak RSS, available 17.6 down to 10.0 GiB), gate $GATE GiB"
python3 -c "import sys; sys.exit(0 if $AVAIL >= $GATE else 1)" || stop "less than $GATE GiB available ($AVAIL)"
HC=$(command -v hc)
cat > $OUT/scan/watch_alert.sh <<'WEOF'
#!/bin/bash
# alert only: hc to t5 when available memory < 2 GiB, free memory < 8% or free disk < 3 GiB (at most one alert per 10 minutes); stops and kills nothing
OUT=$1; HC=$2; last=0
while :; do
  alive=$(pgrep -f "d18_hybsign.py" | wc -l | tr -d ' ')
  [ "$alive" = 0 ] && exit 0
  av=$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')
  fr=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//'); dk=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}')
  now=$(date +%s)
  if python3 -c "import sys; sys.exit(0 if ($av < 2 or $fr < 8 or $dk < 3) else 1)" && [ $((now - last)) -gt 600 ]; then
    msg="macm3 #1025 kc87_leg_lambda ALERT $(date -u '+%F %T') UTC: available memory $av GiB, free memory $fr%, free disk $dk GiB (alert only, nothing stopped)"
    echo "$msg" >> $OUT/alert.log; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$msg" >> $OUT/alert.log 2>&1; last=$now
  fi
  sleep 60
done
WEOF
chmod +x $OUT/scan/watch_alert.sh
nice -n 10 $OUT/scan/watch_alert.sh $OUT "$HC" > /dev/null 2>&1 &
R1=-1; R2=-1; for ((i = 0; i < ${#LAMP[@]}; i++)); do [ "${LAMP[$i]}" = "$REP" ] && { [ $R1 -lt 0 ] && R1=$i || R2=$i; }; done
[ $R2 -ge 0 ] && [ $((R1 % NP)) != $((R2 % NP)) ] || stop "the repeat of $REP is not on another process than the first"
step "scan starts: D $D, ${#LAMP[@]} values (${LAMP[*]}) on $NP processes of 1 thread, nice ${NICE:-10}, round-robin (a process runs its values one after another); the first $REP on process $((R1 % NP)), the repeat on process $((R2 % NP)); state $STATEFILE $(blob $STATE), record $(blob $STUB); alert watcher on (hc: ${HC:-none})"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""; for ((i = p; i < ${#LAMP[@]}; i += NP)); do mine="$mine,${LAMP[$i]}"; done; mine=${mine#,}
  ( cd $WTM && nice -n ${NICE:-10} env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1 \
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
open('$OUT/scan/scan_D${D}_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows)); print(len(rows), 'evaluations,', sum(r['noise_robust'] for r in rows), 'noise-robust')" >> $OUT/steps.txt
grep -h 'the record system\|NOT the record system' $OUT/scan/scan_p*.log | sort | uniq -c >> $OUT/steps.txt
cd $L/common/in
$PY -I read_lower.py selftest > $OUT/selftest_read_lower.txt 2>&1; e0=$?
$PY -I read_lower.py selftest --mutate=shift > $OUT/selftest_read_lower_shift.txt 2>&1; e1=$?
$PY -I read_lower.py selftest --mutate=round2 > $OUT/selftest_read_lower_round2.txt 2>&1; e2=$?
step "read_lower selftest exit $e0 (0 wanted); mutations shift exit $e1, round2 exit $e2 (1 wanted each)"
{ echo "== window: read_lower.py scan $WIN"; $PY -I read_lower.py $OUT/scan $WIN; echo "(exit $?)"; } > $OUT/read_lower.txt 2>&1
step "read_lower.py read the window (reading in read_lower.txt)"
$PY -I repeat_check.py selftest > $OUT/selftest_repeat_check.txt 2>&1; step "repeat_check selftest exit $? (0 wanted)"
$PY -I repeat_check.py $OUT/scan/scan_D${D}_1025.jsonl >> $OUT/read_lower.txt 2>&1; step "repeat_check.py on the merged scan exit $? (0 agree, 1 disagree, 2 no repeat)"
echo "SCAN DONE $(stamp) UTC" > $OUT/SCAN_DONE.txt
step "scan done"
exit 0
}
