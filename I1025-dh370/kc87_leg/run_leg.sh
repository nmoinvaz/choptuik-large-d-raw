#!/bin/bash
# #1025 kc87_leg on dh370 (t5's order, #1025 comment 7120900647): the k_c 87 leg from the seeds D 20.90625 (dh170) and D 21.0 (dh610) to D 21.25, h 0.03125, win2's recipe on Linux, 6 BLAS threads, nice 10, cap 10 h by exact pid.
#   ell_leap.py l1kc87Ldh370 1 87 data/<seed A> 20.90625 data/<seed B> 21.0 21.25 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
# usage: run_leg.sh             the leg (unit i1025leg87)
#        DRY=1 run_leg.sh       the pins, selftests and seed checks only, seed A standing in for both seeds; prints the command, starts nothing, writes only the check outputs under dry/
# Everything is logged to exits_leg.txt; the guard (leap_guard.py with the Linux shims) and the tracker run beside the leap. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
WT=/home/nathan/Source/choptuik-large-d-1025l
WTM=$WT/solver/matter
DATA=$WTM/data
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc87Ldh370
SA=sol_l1kc87dh170e_D20.9062.npy; SB=sol_l1kc87dh610e_D21.0000.npy
DA=20.90625; DB=21.0; DEND=21.25; H=0.03125
stamp() { date -u '+%F %T'; }
log() { echo "kc87_leg $* $(stamp) UTC" >> $OUT/exits_leg.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
export PATH=$OUT/shims:$PATH
cd $OUT || exit 9
if [ "$DRY" = 1 ]; then CHK=$OUT/dry; mkdir -p $CHK; else CHK=$OUT; fi
bad=0
chk() { [ "$(blob "$1")" = "$2" ] || { log "refuse: $3 is blob $(blob "$1"), not $2"; bad=1; }; }
chk $WTM/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/in/leap_guard.py f1fe7c7c "leap_guard.py"
chk $OUT/in/mode_tracker.py 807c2d95 "mode_tracker.py"
chk $OUT/in/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $OUT/in/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/in/seedA_$SA fe200cc6 "seed A state"
chk $OUT/in/seedA_l1kc87dh170e.jsonl 03544bb4 "seed A record"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { log "refuse: the worktree is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { log "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { log "refuse: the worktree's solver/ has changes"; bad=1; }
if [ "$DRY" != 1 ]; then
  chk $OUT/in/seedB_$SB "$(cat $OUT/in/seedB_state.blob 2>/dev/null)" "seed B state"
  chk $OUT/in/seedB_l1kc87dh610e.jsonl "$(cat $OUT/in/seedB_record.blob 2>/dev/null)" "seed B record"
  for f in $DATA/$TAG.jsonl $OUT/leap.log $OUT/leg_STOP.txt $OUT/leg_points.txt $OUT/leap.finished; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
fi
[ $bad = 0 ] || exit 2
log "pins checked: ell_leap.py 1eb873e4, leap_guard.py f1fe7c7c, mode_tracker.py 807c2d95, kc87/kc79 syscheck 6df5d960/29dce7ea, worktree 48c36355 (solver code = 505d8399), seed A fe200cc6/03544bb4; $($PY -V 2>&1); load $(cut -d' ' -f1-3 /proc/loadavg)$([ "$DRY" = 1 ] && echo '; DRY RUN')"
# the tools' controls
$PY in/leap_guard.py --selftest > $CHK/selftest_leap_guard.txt 2>&1; g0=$?
g1=0; for m in slope cos nnull; do $PY in/leap_guard.py --selftest --mutate=$m > $CHK/selftest_leap_guard_mut_$m.txt 2>&1; [ $? = 1 ] || g1=1; done
$PY in/mode_tracker.py --selftest > $CHK/selftest_mode_tracker.txt 2>&1; t0=$?
t1=0; for m in count cos entry bcount bcos; do $PY in/mode_tracker.py --selftest --mutate=$m > $CHK/selftest_mode_tracker_mut_$m.txt 2>&1; [ $? = 1 ] || t1=1; done
$PY in/kc87_syscheck_1025.py --selftest > $CHK/selftest_kc87_syscheck.txt 2>&1; k0=$?
$PY in/kc79_syscheck_1025.py --selftest > $CHK/selftest_kc79_syscheck.txt 2>&1; k1=$?
log "selftests: leap_guard $g0 (0 wanted), its mutations all exit 1: $([ $g1 = 0 ] && echo yes || echo NO); mode_tracker $t0 (0 wanted), its mutations all exit 1: $([ $t1 = 0 ] && echo yes || echo NO); kc87_syscheck $k0, kc79_syscheck $k1 (0 wanted)"
[ $g0 = 0 ] && [ $g1 = 0 ] && [ $t0 = 0 ] && [ $t1 = 0 ] && [ $k0 = 0 ] && [ $k1 = 0 ] || { log "STOP: a selftest or a control did not read as written"; exit 1; }
# the seeds: accepted by the k_c 87 check (controls exit 1), refused by the k_c 79 check
seedcheck() {   # name, record, state, D
  $PY in/kc87_syscheck_1025.py $2 $3 $4 $WTM > $CHK/seed$1_syscheck.txt 2>&1; a0=$?
  $PY in/kc87_syscheck_1025.py $2 $3 $4 $WTM --mutate=F > $CHK/seed$1_syscheck_mutF.txt 2>&1; a1=$?
  $PY in/kc87_syscheck_1025.py $2 $3 $4 $WTM --mutate=steps > $CHK/seed$1_syscheck_mutsteps.txt 2>&1; a2=$?
  $PY in/kc79_syscheck_1025.py $2 $3 $4 $WTM > $CHK/seed$1_kc79_refuses.txt 2>&1; a3=$?
  log "seed $1 (D $4): kc87_syscheck exit $a0 (0 wanted); controls --mutate=F $a1, --mutate=steps $a2 (1 wanted each); kc79_syscheck exit $a3 (1 wanted: it must refuse k_c 87); $(grep -E '^(ACCEPTED|NOT ACCEPTED)' $CHK/seed$1_syscheck.txt | head -1 | cut -c1-200)"
  [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]
}
cp -n $OUT/in/seedA_$SA $DATA/$SA; cp -n $OUT/in/seedA_l1kc87dh170e.jsonl $DATA/l1kc87dh170e.jsonl
if [ "$DRY" = 1 ]; then
  seedcheck A_dry $DATA/l1kc87dh170e.jsonl $DATA/$SA $DA || { log "STOP: seed A was not accepted"; exit 1; }
  echo "DRY: cd $WTM && nice -n 10 timeout -k 120 36000 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_leap.py $TAG 1 87 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
  log "DRY run ended: seed A accepted (seed B's checks wait for its publication)"; exit 0
fi
cp -n $OUT/in/seedB_$SB $DATA/$SB; cp -n $OUT/in/seedB_l1kc87dh610e.jsonl $DATA/l1kc87dh610e.jsonl
seedcheck A $DATA/l1kc87dh170e.jsonl $DATA/$SA $DA || { log "STOP: seed A was not accepted"; exit 1; }
seedcheck B $DATA/l1kc87dh610e.jsonl $DATA/$SB $DB || { log "STOP: seed B was not accepted"; exit 1; }
tail -n 1 $OUT/in/seedA_l1kc87dh170e.jsonl > $OUT/leg_seedA.jsonl; tail -n 1 $OUT/in/seedB_l1kc87dh610e.jsonl > $OUT/leg_seedB.jsonl
CMD="nice -n 10 timeout -k 120 36000 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_leap.py $TAG 1 87 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
echo "== $(stamp) UTC $CMD (cwd $WTM)" > $OUT/leap.log
log "starting the leap: $CMD"
( cd $WTM && exec $CMD >> $OUT/leap.log 2>&1 ) &
pid=$!
log "leap87 root pid $pid"
( $PY $OUT/in/leap_guard.py --rec $DATA/$TAG.jsonl --exits $OUT/exits_leg.txt --rootkey "leap87 root pid" --log $OUT/leap.log --out $OUT/leg_points.txt --stop $OUT/leg_STOP.txt --done $OUT/leap.finished --seeds $OUT/leg_seedA.jsonl $OUT/leg_seedB.jsonl > $OUT/guard.log 2>&1 ) &
gpid=$!
log "guard started (pid $gpid, shims on PATH)"
( echo "time,max_rss_kb,proc,mem_available_kb" > $OUT/mem_samples.csv; while kill -0 $pid 2>/dev/null; do echo "$(date -u +%T),$(ps -eo rss=,comm= --sort=-rss | head -1 | awk '{print $1","$2}'),$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" >> $OUT/mem_samples.csv; sleep 60; done ) &
t0=$(date +%s)
copy() { cp -u $DATA/*$TAG* $OUT/ 2>/dev/null; [ -s $DATA/$TAG.jsonl ] && $PY $OUT/in/mode_tracker.py $DATA/$TAG.jsonl > $OUT/tracker_rows.txt 2>$OUT/tracker_err.txt; }
while kill -0 $pid 2>/dev/null; do sleep 120; copy; done
wait $pid; rc=$?
touch $OUT/leap.finished
sleep 20; copy
log "leap exit $rc wall $(( $(date +%s) - t0 )) s (124/137 = the 10 h cap); $(tail -2 $OUT/leap.log | cut -c1-200 | tr '\n' '|')"
echo "LEG DONE exit $rc $(stamp) UTC" > $OUT/LEG_DONE.txt
exit 0
}
