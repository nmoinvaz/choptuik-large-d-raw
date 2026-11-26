#!/bin/bash
# #1025 macm3 kc87_leg_lambda/pointnew.sh (t5's change of the scanner, hc 26 Nov: "the scanner changes for every scan that has not started"): point87.sh's scan with the NEW scanner, d18_secant.py scan of wip/ell1-speed 92b9bf53
# (blob eb1396ad; the worktree ~/Source/choptuik-large-d-1025s2): per process "python -u d18_secant.py scan STUB.jsonl STATE.npy D LAMS OUT.jsonl --pin=<state blob>,<stub blob>" under capped_run.py, the fast float64 matrix, ell_ddm's block 12, the 1e-15
# noise test; it writes d18_hybsign.py's fields (plus dln, robust, mm) so read_lower.py and repeat_check.py read the merged file unchanged. The state and the record are read from DNAME/in/ (the pinned copies), not from a worktree's data/.
# usage: bash pointnew.sh DNAME scan      (DNAME/point.env: D TAG RAWC STATEFILE STATEBLOB RECBLOB LAMP WIN REP NP; DNAME/VERDICT.txt must start with ACCEPTED, as point87.sh's scan)
# Steps go to DNAME/steps.txt. The scan runs only after ACCEPTED, with at most NP processes (t5: at most 2 for k_c 119).
{
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
DN=$1; MODE=${2:?accept | scan | dry}; OUT=$L/$DN
. $OUT/point.env
WT=$HOME/Source/choptuik-large-d-1025s2; WTM=$WT/solver/matter; WTB=$HOME/Source/choptuik-large-d-1025m
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
chkc kc87_syscheck_1025.py 6df5d960; chkc kc79_syscheck_1025.py 29dce7ea; chkc read_lower.py 89309d3c; chkc d185_scan_read.py 7c9d400f; chkc repeat_check.py aaf598a9
[ "$(blob $WTM/d18_secant.py)" = eb1396ad ] || stop "d18_secant.py of the worktree is not blob eb1396ad"
[ "$(blob $OUT/in/$STATEFILE)" = "$STATEBLOB" ] || stop "in/$STATEFILE is not blob $STATEBLOB"
[ "$(blob $OUT/in/$TAG.jsonl)" = "$RECBLOB" ] || stop "in/$TAG.jsonl is not blob $RECBLOB"
step "inputs pinned: state $STATEBLOB and record $RECBLOB from raw $RAWC (pins.txt); the scanner d18_secant.py eb1396ad (worktree 92b9bf53); kc87_syscheck 6df5d960, kc79_syscheck 29dce7ea, read_lower 89309d3c, d185_scan_read 7c9d400f, repeat_check aaf598a9"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 92b9bf53 ] || stop "worktree not at 92b9bf53"
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $WTM/$f.py)" = "$(blob $WTB/solver/matter/$f.py)" ] || stop "$f.py differs from the scan worktree 505d8399 files"; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 92b9bf53 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399's), clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
STATE=$OUT/in/$STATEFILE; STUB=$OUT/in/$TAG.jsonl
if [ "$MODE" = dry ]; then step "dry run: pins and worktree ok, nothing started; values ${LAMP[*]}"; echo "dry ok"; exit 0; fi

# MODE = scan
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
[ -e $OUT/SCAN_DONE.txt ] || [ -z "$(ls $OUT/scan 2>/dev/null)" ] || stop "scan/ is not empty"
[ "$(blob $STATE)" = "$STATEBLOB" ] && [ "$(blob $STUB)" = "$RECBLOB" ] || stop "the state or record differs from the pin"
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
  alive=$(pgrep -f "d18_secant.py scan" | wc -l | tr -d ' ')
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
  ( cd $WTM && nice -n ${NICE:-10} env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1 \
      $PY -u $L/common/capped_run.py 28800 $PY -u $WTM/d18_secant.py scan $STUB $STATE $D "$mine" $OUT/scan/scan_D${D}_p$p.jsonl --pin=$STATEBLOB,$RECBLOB > $OUT/scan/scan_p$p.log 2>&1
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
