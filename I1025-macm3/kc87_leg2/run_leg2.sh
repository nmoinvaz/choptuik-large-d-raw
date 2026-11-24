#!/bin/bash
# #1025 macm3 kc87_leg2 (t5's order, hc 24 Nov, corrected to h 0.0625): the k_c 87 leg from dh370's D 21.21875 and D 21.25 states on to D 21.5, ell_leap.py at 48c36355, 4 BLAS threads, nice 10, cap 12 h by exact pid.
#   ell_leap.py l1kc87Lmacm3 1 87 data/<seed A> 21.21875 data/<seed B> 21.25 21.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
# usage: run_leg2.sh dry   the pins, selftests, controls and seed checks only; prints the command, starts nothing (writes only under checks/ and exits_leg2.txt)
#        run_leg2.sh run   the same, then the leg with its guard (pinned leap_guard.py + shims_mac/), watchdog (3 h per point), sampler, alert watcher, and per-point copy and push
# Everything is logged to exits_leg2.txt. No hc from here except the memory alerts (alert only).
{
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
WT=$HOME/Source/choptuik-large-d-1025m2; WTM=$WT/solver/matter; DATA=$WTM/data
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc87Lmacm3
SA=sol_l1kc87Ldh370_D21.218750.npy; SB=sol_l1kc87Ldh370_D21.250000.npy; DA=21.21875; DB=21.25; DEND=21.5; H=0.0625
MODE=${1:?dry or run}
stamp() { date -u '+%F %T'; }
log() { echo "kc87_leg2 $* $(stamp) UTC" >> $L2/exits_leg2.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
export PATH=$L2/shims_mac:$PATH
cd $L2 || exit 9
CHK=$L2/checks; mkdir -p $CHK
bad=0
chk() { [ "$(blob "$1")" = "$2" ] || { log "refuse: $3 is blob $(blob "$1"), not $2"; bad=1; }; }
chk $WTM/ell_leap.py 1eb873e4 "ell_leap.py"
chk in/leap_guard.py f1fe7c7c "leap_guard.py"
chk in/mode_tracker.py 807c2d95 "mode_tracker.py"
chk in/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk in/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk in/capped_run.py 11f0647b "capped_run.py"
chk shims_mac/powershell bb793d6b "shims_mac/powershell"
chk shims_mac/taskkill fc17147c "shims_mac/taskkill"
chk in/$SA dbc66a07 "seed A state"
chk in/$SB 7e88c368 "seed B state"
chk in/l1kc87Ldh370.jsonl 07eef60f "seeds' record"
chk $DATA/$SA dbc66a07 "seed A state in data/"
chk $DATA/$SB 7e88c368 "seed B state in data/"
chk $DATA/l1kc87Ldh370.jsonl 07eef60f "seeds' record in data/"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { log "refuse: the worktree is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { log "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { log "refuse: the worktree's solver/ has changes"; bad=1; }
if [ "$MODE" = run ]; then
  for f in $DATA/$TAG.jsonl $L2/leap.log $L2/leg_STOP.txt $L2/leg_points.txt $L2/leap.finished $L2/leap.started $L2/pushed_points.txt; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
fi
[ $bad = 0 ] || exit 2
log "pins checked ($MODE): ell_leap.py 1eb873e4, leap_guard.py f1fe7c7c, mode_tracker.py 807c2d95, kc87/kc79 syscheck 6df5d960/29dce7ea, capped_run.py 11f0647b, shims_mac bb793d6b/fc17147c, worktree 48c36355 (solver code = 505d8399), seeds dbc66a07/7e88c368/07eef60f; $($PY -V 2>&1); load $(sysctl -n vm.loadavg | tr -d '{}')"
# the tools' controls
$PY in/leap_guard.py --selftest > $CHK/selftest_leap_guard.txt 2>&1; g0=$?
g1=0; for m in slope cos nnull; do $PY in/leap_guard.py --selftest --mutate=$m > $CHK/selftest_leap_guard_mut_$m.txt 2>&1; [ $? = 1 ] || g1=1; done
$PY in/mode_tracker.py --selftest > $CHK/selftest_mode_tracker.txt 2>&1; t0=$?
t1=0; for m in count cos entry bcount bcos; do $PY in/mode_tracker.py --selftest --mutate=$m > $CHK/selftest_mode_tracker_mut_$m.txt 2>&1; [ $? = 1 ] || t1=1; done
$PY in/kc87_syscheck_1025.py --selftest > $CHK/selftest_kc87_syscheck.txt 2>&1; k0=$?
$PY in/kc79_syscheck_1025.py --selftest > $CHK/selftest_kc79_syscheck.txt 2>&1; k1=$?
$PY leg_watch.py --selftest > $CHK/selftest_leg_watch.txt 2>&1; w0=$?
$PY leg_watch.py --selftest --mutate=cap > $CHK/selftest_leg_watch_mut_cap.txt 2>&1; w1=$?
$PY dry_guard_pid.py > $CHK/dry_guard_pid.txt 2>&1; d0=$?
$PY dry_guard_pid.py --mutate=decoy > $CHK/dry_guard_pid_mut_decoy.txt 2>&1; d1=$?
log "selftests: leap_guard $g0 (0 wanted), its mutations all exit 1: $([ $g1 = 0 ] && echo yes || echo NO); mode_tracker $t0 (0 wanted), its mutations all exit 1: $([ $t1 = 0 ] && echo yes || echo NO); kc87_syscheck $k0, kc79_syscheck $k1 (0 wanted); leg_watch $w0 (0 wanted), its --mutate=cap $w1 (1 wanted); dry_guard_pid $d0 (0 wanted), its --mutate=decoy $d1 (1 wanted)"
[ $g0 = 0 ] && [ $g1 = 0 ] && [ $t0 = 0 ] && [ $t1 = 0 ] && [ $k0 = 0 ] && [ $k1 = 0 ] && [ $w0 = 0 ] && [ $w1 = 1 ] && [ $d0 = 0 ] && [ $d1 = 1 ] || { log "STOP: a selftest or a control did not read as written"; exit 1; }
# the tracker on dh370's record reproduces dh370's published rows (and a changed rows file differs)
$PY in/mode_tracker.py in/l1kc87Ldh370.jsonl > $CHK/tracker_dh370_reproduced.txt 2> $CHK/tracker_dh370_err.txt; tr0=$?
diff -q $CHK/tracker_dh370_reproduced.txt in/dh370_tracker_rows.txt > /dev/null; tr1=$?
sed '$d' in/dh370_tracker_rows.txt | diff -q $CHK/tracker_dh370_reproduced.txt - > /dev/null; tr2=$?
log "tracker on dh370's record: exit $tr0, rows identical to dh370's published tracker_rows.txt (diff exit $tr1, 0 wanted); against that file without its last row diff exit $tr2 (1 wanted)"
[ $tr0 = 0 ] && [ $tr1 = 0 ] && [ $tr2 = 1 ] || { log "STOP: the tracker does not reproduce dh370's rows"; exit 1; }
# the seeds: accepted by the k_c 87 check (controls exit 1), refused by the k_c 79 check
seedcheck() {   # name, state, D
  $PY in/kc87_syscheck_1025.py $DATA/l1kc87Ldh370.jsonl $DATA/$2 $3 $WTM > $CHK/seed$1_syscheck.txt 2>&1; a0=$?
  $PY in/kc87_syscheck_1025.py $DATA/l1kc87Ldh370.jsonl $DATA/$2 $3 $WTM --mutate=F > $CHK/seed$1_syscheck_mutF.txt 2>&1; a1=$?
  $PY in/kc87_syscheck_1025.py $DATA/l1kc87Ldh370.jsonl $DATA/$2 $3 $WTM --mutate=steps > $CHK/seed$1_syscheck_mutsteps.txt 2>&1; a2=$?
  $PY in/kc79_syscheck_1025.py $DATA/l1kc87Ldh370.jsonl $DATA/$2 $3 $WTM > $CHK/seed$1_kc79_refuses.txt 2>&1; a3=$?
  log "seed $1 (D $3): kc87_syscheck exit $a0 (0 wanted); controls --mutate=F $a1, --mutate=steps $a2 (1 wanted each); kc79_syscheck exit $a3 (1 wanted: it must refuse k_c 87); $(grep -E '^(ACCEPTED|NOT ACCEPTED)' $CHK/seed$1_syscheck.txt | head -1 | cut -c1-200)"
  [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]
}
seedcheck A $SA $DA || { log "STOP: seed A was not accepted"; exit 1; }
seedcheck B $SB $DB || { log "STOP: seed B was not accepted"; exit 1; }
CMD="nice -n 10 $PY -u $L2/in/capped_run.py 43200 env OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 $PY -u ell_leap.py $TAG 1 87 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$MODE" = dry ]; then
  echo "DRY: cd $WTM && $CMD"
  log "DRY run ended: pins, selftests, controls and both seeds accepted; the command: $CMD"; exit 0
fi
echo "== $(stamp) UTC $CMD (cwd $WTM)" > $L2/leap.log
log "starting the leap: $CMD"
( cd $WTM && exec $CMD >> $L2/leap.log 2>&1 ) &
pid=$!
date +%s > $L2/leap.started; touch $L2/leap.started
log "leap87 root pid $pid"
( $PY $L2/in/leap_guard.py --rec $DATA/$TAG.jsonl --exits $L2/exits_leg2.txt --rootkey "leap87 root pid" --log $L2/leap.log --out $L2/leg_points.txt --stop $L2/leg_STOP.txt --done $L2/leap.finished --seeds $L2/leg_seedA.jsonl $L2/leg_seedB.jsonl > $L2/guard.log 2>&1 ) &
log "guard started (pid $!, shims_mac first on PATH)"
( $PY $L2/leg_watch.py --rec $DATA/$TAG.jsonl --since $L2/leap.started --exits $L2/exits_leg2.txt --rootkey "leap87 root pid" --stop $L2/leg_STOP.txt --done $L2/leap.finished --cap 10800 > $L2/watch.log 2>&1 ) &
log "watchdog started (pid $!, 3 h per point)"
nice -n 10 $L2/watch_alert_leg.sh $L2 "$(command -v hc)" > /dev/null 2>&1 &
( echo "time_utc,leap_rss_kb,scan_rss_kb,avail_GiB,free_mem_pct" > $L2/mem_samples.csv
  while kill -0 $pid 2>/dev/null; do
    lp=$(pgrep -P $pid | head -1); lr=0; [ -n "$lp" ] && lr=$(ps -o rss= -p $lp | tr -d ' ')
    sr=$(ps -axo rss=,command= | awk '/d18_hybsign/ && !/awk/ {s+=$1} END {print s+0}')
    av=$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')
    fr=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//')
    echo "$(date -u +%T),${lr:-0},$sr,$av,$fr" >> $L2/mem_samples.csv; sleep 60
  done ) &
t0=$(date +%s)
pointpush() {   # every record with its state not yet pushed: copy, tracker rows, push, log
  for D in $($PY $L2/new_points.py $DATA/$TAG.jsonl $DATA $TAG $L2/pushed_points.txt); do
    sleep 20      # the leap writes the record line and the states in one pass; settle
    rsync -a $DATA/sol_${TAG}_* $DATA/$TAG.jsonl $L2/
    $PY $L2/in/mode_tracker.py $L2/in/l1kc87Ldh370.jsonl $DATA/$TAG.jsonl > $L2/tracker_rows.txt 2> $L2/tracker_err.txt
    out=$(bash $L2/push_leg2.sh "kc87_leg2: the state and record of D $D (for the scan)" 2>&1 | tail -1)
    S=$(printf "sol_${TAG}_D%.6f.npy" $D)
    log "point D $D: $out; state $S blob $(blob $L2/$S), record $TAG.jsonl blob $(blob $L2/$TAG.jsonl) ($(grep -c . $L2/$TAG.jsonl) lines)"
    case "$out" in pushed*) echo "$D" >> $L2/pushed_points.txt;; esac
  done
}
while kill -0 $pid 2>/dev/null; do sleep 60; pointpush; done
wait $pid; rc=$?
touch $L2/leap.finished
sleep 25; pointpush
tb=$(grep -c Traceback $L2/leap.log)
log "leap exit $rc wall $(( $(date +%s) - t0 )) s (124/137/143 = the cap or a kill); Tracebacks in leap.log: $tb; $([ -e $L2/leg_STOP.txt ] && echo "STOP file: $(head -1 $L2/leg_STOP.txt | cut -c1-200)" || echo 'no STOP file'); $(tail -2 $L2/leap.log | cut -c1-200 | tr '\n' '|')"
echo "LEG DONE exit $rc $(stamp) UTC" > $L2/LEG_DONE.txt
bash $L2/push_leg2.sh "kc87_leg2: the leg ends (exit $rc)" 2>&1 | tail -1 >> $L2/exits_leg2.txt
exit 0
}
