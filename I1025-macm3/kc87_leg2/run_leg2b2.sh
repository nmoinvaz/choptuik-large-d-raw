#!/bin/bash
# #1025 macm3 kc87_leg2 PART B2 (t5's order, hc 24 Nov 19:4x UTC): part b stopped at D 21.96875 by LinAlgError 'SVD did not converge' in ell_leap.py's fold block (the D 22.0 step; numpy's Accelerate gesdd on a finite J, rerun in scratchpad/svd22).
# t5's fix (wip/ell1-highD edf49057, ell_leap.py blob 5816d7b3: the fold block calls dss_ell.svd_robust; each fold record adds delta_reg). Part b2 restarts from part b's D 21.9375 and D 21.96875 states to D 22.5 at h 0.03125,
# same guard, shims, checks, watchdog and cap; the only pin changed is ell_leap.py 5816d7b3 in place of 1eb873e4 (worktree ~/Source/choptuik-large-d-1025m3 at edf49057; the solver files other than ell_leap.py are those of 505d8399, checked).
#   ell_leap.py l1kc87Lmacm3b2 1 87 data/<D 21.9375 state> 21.9375 data/<D 21.96875 state> 21.96875 22.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold   (4 BLAS threads, nice 10, cap 12 h by exact pid)
# Outputs go to kc87_leg2/b2/ (exits_leg2b2.txt, leap.log, guard.log, leg_points.txt, tracker_rows.txt, mem_samples.csv, pushed_points.txt, the states and the record l1kc87Lmacm3b2.jsonl).
# usage: run_leg2b2.sh dry   the pins, selftests, controls and seed checks only; prints the command, starts nothing (writes only under b2/checks/ and b2/exits_leg2b2.txt)
#        run_leg2b2.sh run   the same, then the leg with its guard (pinned leap_guard.py + shims_mac/), watchdog (3 h per point), sampler, alert watcher, and per-point copy and push
# Everything is logged to exits_leg2b2.txt. No hc from here except the memory alerts (alert only).
{
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
WT=$HOME/Source/choptuik-large-d-1025m3; WTM=$WT/solver/matter; DATA=$WTM/data
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=${TAGB2:-l1kc87Lmacm3b2}; PREV=l1kc87Lmacm3; PREVB=l1kc87Lmacm3b          # PREV, PREVB: part a's and part b's tags (part b's states and record are the seeds)
SA=${SAB2:-sol_l1kc87Lmacm3b_D21.937500.npy}; SB=${SBB2:-sol_l1kc87Lmacm3b_D21.968750.npy}; DA=${DAB2:-21.9375}; DB=${DBB2:-21.96875}; DEND=22.5; H=0.03125
SEEDREC=${SEEDRECB2:-$DATA/$PREVB.jsonl}                # the record file holding the seeds' rows
MODE=${1:?dry or run}
stamp() { date -u '+%F %T'; }
B=$L2/b2; mkdir -p $B
log() { echo "kc87_leg2b2 $* $(stamp) UTC" >> $B/exits_leg2b2.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
export PATH=$L2/shims_mac:$PATH
cd $L2 || exit 9
CHK=$B/checks; mkdir -p $CHK
bad=0
chk() { [ "$(blob "$1")" = "$2" ] || { log "refuse: $3 is blob $(blob "$1"), not $2"; bad=1; }; }
chk $WTM/ell_leap.py 5816d7b3 "ell_leap.py"
chk in/leap_guard.py f1fe7c7c "leap_guard.py"
chk in/mode_tracker.py 807c2d95 "mode_tracker.py"
chk in/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk in/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk in/capped_run.py 11f0647b "capped_run.py"
chk shims_mac/powershell bb793d6b "shims_mac/powershell"
chk shims_mac/taskkill fc17147c "shims_mac/taskkill"
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
git -C $RAWG fetch -q
rawblob() { git -C $RAWG rev-parse --short=8 origin/main:$1 2>/dev/null; }
chk in/l1kc87Ldh370.jsonl 07eef60f "dh370's record"
SAB8=$(rawblob I1025-macm3/kc87_leg2/b/$SA); SBB8=$(rawblob I1025-macm3/kc87_leg2/b/$SB); RECB8=$(rawblob I1025-macm3/kc87_leg2/b/$PREVB.jsonl)
[ -n "$SAB8" ] && [ -n "$SBB8" ] && [ -n "$RECB8" ] || { log "refuse: the seeds or the record of part b are not on raw (I1025-macm3/kc87_leg2/b/)"; bad=1; }
chk $DATA/$SA "$SAB8" "seed A state in data/ (the raw copy's blob)"
chk $DATA/$SB "$SBB8" "seed B state in data/ (the raw copy's blob)"
[ "$MODE" = run ] && [ "$(blob $SEEDREC)" != "$RECB8" ] && { log "refuse: part b's record in data/ is blob $(blob $SEEDREC), the raw copy is $RECB8"; bad=1; }
[ "$(git -C $WT rev-parse --short=8 HEAD)" = edf49057 ] || { log "refuse: the worktree is not at edf49057"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { log "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { log "refuse: the worktree's solver/ has changes"; bad=1; }
if [ "$MODE" = run ]; then
  for f in $DATA/$TAG.jsonl $B/leap.log $B/leg_STOP.txt $B/leg_points.txt $B/leap.finished $B/leap.started $B/pushed_points.txt; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
fi
[ $bad = 0 ] || exit 2
log "pins checked ($MODE): ell_leap.py 5816d7b3 (was 1eb873e4 in parts a and b and the control), leap_guard.py f1fe7c7c, mode_tracker.py 807c2d95, kc87/kc79 syscheck 6df5d960/29dce7ea, capped_run.py 11f0647b, shims_mac bb793d6b/fc17147c, worktree edf49057 (solver code other than ell_leap.py = 505d8399), seeds $SA $SAB8 and $SB $SBB8 (raw copies of part b), part b's record $RECB8; $($PY -V 2>&1); load $(sysctl -n vm.loadavg | tr -d '{}')"
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
  $PY in/kc87_syscheck_1025.py $SEEDREC $DATA/$2 $3 $WTM > $CHK/seed$1_syscheck.txt 2>&1; a0=$?
  $PY in/kc87_syscheck_1025.py $SEEDREC $DATA/$2 $3 $WTM --mutate=F > $CHK/seed$1_syscheck_mutF.txt 2>&1; a1=$?
  $PY in/kc87_syscheck_1025.py $SEEDREC $DATA/$2 $3 $WTM --mutate=steps > $CHK/seed$1_syscheck_mutsteps.txt 2>&1; a2=$?
  $PY in/kc79_syscheck_1025.py $SEEDREC $DATA/$2 $3 $WTM > $CHK/seed$1_kc79_refuses.txt 2>&1; a3=$?
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
python3 - "$SEEDREC" "$DA" "$DB" "$B" <<'PY' || { log "STOP: the seeds' rows were not found"; exit 1; }
import json, sys
rec, da, db, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
rows = [json.loads(l) for l in open(rec) if l.strip()]
for D, name in ((da, "leg_seedA.jsonl"), (db, "leg_seedB.jsonl")):
    r = [x for x in rows if x["D"] == D][-1]
    open(b + "/" + name, "w").write(json.dumps(r) + "\n")
PY
echo "== $(stamp) UTC $CMD (cwd $WTM)" > $B/leap.log
log "starting the leap: $CMD"
( cd $WTM && exec $CMD >> $B/leap.log 2>&1 ) &
pid=$!
date +%s > $B/leap.started; touch $B/leap.started
log "leap87b2 root pid $pid"
( $PY $L2/in/leap_guard.py --rec $DATA/$TAG.jsonl --exits $B/exits_leg2b2.txt --rootkey "leap87b2 root pid" --log $B/leap.log --out $B/leg_points.txt --stop $B/leg_STOP.txt --done $B/leap.finished --seeds $B/leg_seedA.jsonl $B/leg_seedB.jsonl > $B/guard.log 2>&1 ) &
log "guard started (pid $!, shims_mac first on PATH)"
( $PY $L2/leg_watch.py --rec $DATA/$TAG.jsonl --since $B/leap.started --exits $B/exits_leg2b2.txt --rootkey "leap87b2 root pid" --stop $B/leg_STOP.txt --done $B/leap.finished --cap 10800 > $B/watch.log 2>&1 ) &
log "watchdog started (pid $!, 3 h per point)"
nice -n 10 $L2/watch_alert_leg.sh $B "$(command -v hc)" > /dev/null 2>&1 &
( echo "time_utc,leap_rss_kb,scan_rss_kb,avail_GiB,free_mem_pct" > $B/mem_samples.csv
  while kill -0 $pid 2>/dev/null; do
    lp=$(pgrep -P $pid | head -1); lr=0; [ -n "$lp" ] && lr=$(ps -o rss= -p $lp | tr -d ' ')
    sr=$(ps -axo rss=,command= | awk '/d18_hybsign/ && !/awk/ {s+=$1} END {print s+0}')
    av=$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')
    fr=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//')
    echo "$(date -u +%T),${lr:-0},$sr,$av,$fr" >> $B/mem_samples.csv; sleep 60
  done ) &
t0=$(date +%s)
pointpush() {   # every record with its state not yet pushed: copy, tracker rows, push, log
  for D in $($PY $L2/new_points.py $DATA/$TAG.jsonl $DATA $TAG $B/pushed_points.txt); do
    sleep 20      # the leap writes the record line and the states in one pass; settle
    rsync -a $DATA/sol_${TAG}_* $DATA/$TAG.jsonl $B/
    $PY $L2/in/mode_tracker.py $L2/in/l1kc87Ldh370.jsonl $DATA/$PREV.jsonl $DATA/$PREVB.jsonl $DATA/$TAG.jsonl > $B/tracker_rows.txt 2> $B/tracker_err.txt
    out=$(bash $L2/push_leg2.sh "kc87_leg2b2: the state and record of D $D (for the scan)" 2>&1 | tail -1)
    S=$(printf "sol_${TAG}_D%.6f.npy" $D)
    log "point D $D: $out; state $S blob $(blob $B/$S), record $TAG.jsonl blob $(blob $B/$TAG.jsonl) ($(grep -c . $B/$TAG.jsonl) lines)"
    case "$out" in pushed*) echo "$D" >> $B/pushed_points.txt;; esac
  done
}
while kill -0 $pid 2>/dev/null; do sleep 60; pointpush; done
wait $pid; rc=$?
touch $B/leap.finished
sleep 25; pointpush
tb=$(grep -c Traceback $B/leap.log)
log "leap exit $rc wall $(( $(date +%s) - t0 )) s (124/137/143 = the cap or a kill); Tracebacks in leap.log: $tb; $([ -e $B/leg_STOP.txt ] && echo "STOP file: $(head -1 $B/leg_STOP.txt | cut -c1-200)" || echo 'no STOP file'); $(tail -2 $B/leap.log | cut -c1-200 | tr '\n' '|')"
echo "LEG DONE exit $rc $(stamp) UTC" > $B/LEG_DONE.txt
bash $L2/push_leg2.sh "kc87_leg2b2: the leg ends (exit $rc)" 2>&1 | tail -1 >> $B/exits_leg2b2.txt
exit 0
}
