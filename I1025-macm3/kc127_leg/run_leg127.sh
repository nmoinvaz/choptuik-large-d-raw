#!/bin/bash
# #1025 macm3 kc127_leg (t5's orders, hc 26 Nov ~15:23 and ~15:30 UTC by t5's clock): ONE leg step of k_c 127 from D 23.0625 to D 23.125 with the recipe of kc127_leg (ell_leap.py 5816d7b3 with the guard leap_guard.py f1fe7c7c, stop at max cos_t_reg >= 0.5; h 0.0625; --tol 1e-12
# --fmax 1e-8 --cmax 2e-2 --fold), seeds A = winb's accepted k_c 127 state at D 23.0 (raw I1025-win/kc127_d23: state blob 7a1b150c, record blob eea03461) and B = my accepted k_c 127 state at D 23.0625 (raw I1025-macm3/kc127_d230625/in: state blob 7aae10c6,
# record blob 85a685f1); both seeds are checked first on this machine by the k_c 127 check (exit 0, controls exit 1 1; the k_c 119 and k_c 111 checks refuse them). One k_c 127 job at a time (t5): the point scan and secant start after the leap ends.
# Derived from kc127_leg/run_leg127.sh by explicit replacements. Stops (hc to t5): a pin, selftest or control that does not read as written, a seed not accepted, an exception, the guard firing (its line is reported, the step is not forced), a step over 8 h.
# usage: run_leg127.sh dry | run
{
K=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc127_leg
WT=$HOME/Source/choptuik-large-d-1025m3; WTM=$WT/solver/matter; DATA=$WTM/data
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc127Lmacm3
SA=sol_l1kc127wind23_D23.0000.npy; SB=sol_l1kc127macm3d230625_D23.0625.npy; DA=23.0; DB=23.0625; DEND=23.125; H=0.0625
RECA=$K/in/l1kc127wind23.jsonl; RECB=$K/in/l1kc127macm3d230625.jsonl
MODE=${1:?dry or run}
stamp() { date -u '+%F %T'; }
B=$K; LOGF=$B/exits_leg127.txt
log() { echo "kc127_leg $* $(stamp) UTC" >> $LOGF; }
HC=$(command -v hc)
tell() { log "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOGF 2>&1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
export PATH=$K/shims_mac:$PATH PYTHONDONTWRITEBYTECODE=1
cd $K || exit 9
CHK=$B/checks; mkdir -p $CHK $B/states
bad=0
while read bb f; do case "$bb" in "#"*) continue;; esac
  [ -f $K/$f ] && [ "$(blob $K/$f)" = "$bb" ] || { log "refuse: $f missing or not blob $bb"; bad=1; }; done < $K/in_blobs.txt
chk() { [ "$(blob "$1")" = "$2" ] || { log "refuse: $3 is blob $(blob "$1"), not $2"; bad=1; }; }
chk $WTM/ell_leap.py 5816d7b3 "ell_leap.py"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py 2>/dev/null || { log "refuse: $f.py differs from 505d8399 (or 505d8399 is unknown in $WT)"; bad=1; }; done
[ "$(git -C $WT rev-parse --short=8 HEAD)" = edf49057 ] || { log "refuse: the worktree is not at edf49057"; bad=1; }
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { log "refuse: the worktree's solver/ has changes"; bad=1; }
# the seeds in the worktree's data/ (copied, blob checked)
for s in $SA $SB; do
  [ -e $DATA/$s ] || cp $K/in/$s $DATA/$s
  chk $DATA/$s "$(blob $K/in/$s)" "seed state $s in data/"
done
if [ "$MODE" = run ]; then
  for f in $DATA/$TAG.jsonl $B/leap.log $B/leg_STOP.txt $B/leg_points.txt $B/leap.finished $B/leap.started $B/pushed_points.txt; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
fi
[ $bad = 0 ] || exit 2
log "pins checked ($MODE): in_blobs.txt (seed A winb's state 7a1b150c and record eea03461, seed B my state 7aae10c6 and record 85a685f1, kc127/kc119/kc111 checks 898ebefa/fc6e0dd6/85aeb312, leap_guard f1fe7c7c, capped_run 11f0647b, shims), ell_leap.py 5816d7b3, worktree edf49057 (solver code other than ell_leap.py = 505d8399); $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# the tools' controls
$PY in/leap_guard.py --selftest > $CHK/selftest_leap_guard.txt 2>&1; g0=$?
g1=0; for m in slope cos nnull; do $PY in/leap_guard.py --selftest --mutate=$m > $CHK/selftest_leap_guard_mut_$m.txt 2>&1; [ $? = 1 ] || g1=1; done
$PY leg_watch.py --selftest > $CHK/selftest_leg_watch.txt 2>&1; w0=$?
$PY leg_watch.py --selftest --mutate=cap > $CHK/selftest_leg_watch_mut_cap.txt 2>&1; w1=$?
$PY dry_guard_pid.py > $CHK/dry_guard_pid.txt 2>&1; d0=$?
$PY dry_guard_pid.py --mutate=decoy > $CHK/dry_guard_pid_mut_decoy.txt 2>&1; d1=$?
$PY -I in/kc111_syscheck_1025.py --selftest > $CHK/selftest_kc111_syscheck.txt 2>&1; k0=$?
$PY -I in/kc119_syscheck_1025.py --selftest > $CHK/selftest_kc119_syscheck.txt 2>&1; k1=$?
$PY -I in/kc127_syscheck_1025.py --selftest > $CHK/selftest_kc127_syscheck.txt 2>&1; k2=$?
log "selftests: leap_guard $g0 (0 wanted), its mutations slope cos nnull all exit 1: $([ $g1 = 0 ] && echo yes || echo NO); leg_watch $w0 (0 wanted), its --mutate=cap $w1 (1 wanted); dry_guard_pid $d0 (0 wanted), its --mutate=decoy $d1 (1 wanted); kc111_syscheck $k0, kc119_syscheck $k1, kc127_syscheck $k2 (0 wanted)"
[ $g0 = 0 ] && [ $g1 = 0 ] && [ $w0 = 0 ] && [ $w1 = 1 ] && [ $d0 = 0 ] && [ $d1 = 1 ] && [ $k0 = 0 ] && [ $k1 = 0 ] && [ $k2 = 0 ] || { tell "macm3 #1025 kc127_leg STOP: a selftest or a control did not read as written (see $CHK)"; exit 1; }
# the seeds: accepted by the k_c 103 check (controls exit 1 1); refused by the k_c 95 and k_c 87 checks
seedcheck() {   # name, record, state, D
  a=""; C127="$PY -I in/kc127_syscheck_1025.py $2 $DATA/$3 $4 $WTM"
  $C127 > $CHK/seed$1_kc127.txt 2>&1; a="$?"; $C127 --mutate=F > $CHK/seed$1_kc127_mutF.txt 2>&1; a="$a $?"; $C127 --mutate=steps > $CHK/seed$1_kc127_mutsteps.txt 2>&1; a="$a $?"
  $PY -I in/kc119_syscheck_1025.py $2 $DATA/$3 $4 $WTM > $CHK/seed$1_kc119_refuses.txt 2>&1; a="$a $?"
  $PY -I in/kc111_syscheck_1025.py $2 $DATA/$3 $4 $WTM > $CHK/seed$1_kc111_refuses.txt 2>&1; a="$a $?"
  log "seed $1 (D $4): kc127_syscheck, its controls --mutate=F and --mutate=steps, kc119_syscheck, kc111_syscheck exits: $a (wanted 0 1 1 1 1); $(grep -E '^D ' $CHK/seed$1_kc127.txt | head -1 | cut -c1-220)"
  [ "$a" = "0 1 1 1 1" ]
}
seedcheck A $RECA $SA $DA || { tell "macm3 #1025 kc127_leg STOP: seed A (winb's k_c 127 state at D 23.0) was not accepted as written"; exit 1; }
seedcheck B $RECB $SB $DB || { tell "macm3 #1025 kc127_leg STOP: seed B (my k_c 127 state at D 23.0625) was not accepted as written"; exit 1; }
CMD="nice -n 10 $PY -u $K/in/capped_run.py 43200 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_leap.py $TAG 1 127 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold"
if [ "$MODE" = dry ]; then
  echo "DRY: cd $WTM && $CMD"
  log "DRY run ended: pins, selftests, controls and both seeds accepted; the command: $CMD"; exit 0
fi
python3 - "$RECA" "$RECB" "$DA" "$DB" "$B" <<'PY' || { log "STOP: the seeds' rows were not found"; exit 1; }
import json, sys
ra, rb, da, db, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
for rec, D, name in ((ra, da, "leg_seedA.jsonl"), (rb, db, "leg_seedB.jsonl")):
    r = [x for x in (json.loads(l) for l in open(rec) if l.strip()) if x["D"] == D][-1]
    open(b + "/" + name, "w").write(json.dumps(r) + "\n")
PY
# memory: wait for 8 GiB available (alert only after)
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
n=0; until [ "$(echo "$(availgib) >= 8" | bc)" = 1 ]; do n=$((n+1)); [ $n -gt 360 ] && { tell "macm3 #1025 kc127_leg STOP: less than 8 GiB available for 3 h"; exit 1; }; sleep 30; done
echo "== $(stamp) UTC $CMD (cwd $WTM)" > $B/leap.log
log "starting the leap: $CMD"
( cd $WTM && exec $CMD >> $B/leap.log 2>&1 ) &
pid=$!
date +%s > $B/leap.started; touch $B/leap.started
log "leap127 root pid $pid"
( $PY $K/in/leap_guard.py --rec $DATA/$TAG.jsonl --exits $LOGF --rootkey "leap127 root pid" --log $B/leap.log --out $B/leg_points.txt --stop $B/leg_STOP.txt --done $B/leap.finished --seeds $B/leg_seedA.jsonl $B/leg_seedB.jsonl > $B/guard.log 2>&1 ) &
log "guard started (pid $!, shims_mac first on PATH, --seeds = the two seed rows)"
( $PY $K/leg_watch.py --rec $DATA/$TAG.jsonl --since $B/leap.started --exits $LOGF --rootkey "leap127 root pid" --stop $B/leg_STOP.txt --done $B/leap.finished --cap 21600 > $B/watch.log 2>&1 ) &
log "watchdog started (pid $!, 6 h per point)"
nice -n 10 $K/watch_alert_leg.sh $B "$HC" > /dev/null 2>&1 &
( echo "time_utc,leap_rss_kb,scan_rss_kb,avail_GiB,free_mem_pct" > $B/mem_samples.csv
  while kill -0 $pid 2>/dev/null; do
    lp=$(pgrep -P $pid | head -1); lr=0; [ -n "$lp" ] && lr=$(ps -o rss= -p $lp | tr -d ' ')
    sr=$(ps -axo rss=,command= | awk '/d18_hybsign|d18_secant/ && !/awk/ {s+=$1} END {print s+0}')
    fr=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//')
    echo "$(date -u +%T),${lr:-0},$sr,$(availgib),$fr" >> $B/mem_samples.csv; sleep 60
  done ) &
t0=$(date +%s)
pointpush() {   # every record with its state not yet pushed: copy, push, ready marker, log
  for D in $($PY $K/new_points.py $DATA/$TAG.jsonl $DATA $TAG $B/pushed_points.txt); do
    sleep 20      # the leap writes the record line and the states in one pass; settle
    rsync -a $DATA/sol_${TAG}_* $DATA/$TAG.jsonl $B/states/
    S=$(printf "sol_${TAG}_D%.6f.npy" $D)
    echo "D $D state $S blob $(blob $B/states/$S) record $TAG.jsonl blob $(blob $B/states/$TAG.jsonl) ($(grep -c . $B/states/$TAG.jsonl) lines) $(stamp) UTC" > $B/ready_D$D.txt
    out=$(bash $K/push_leg127.sh "kc127_leg: the state and record of D $D (for the scan)" 2>&1 | tail -1)
    log "point D $D: $out; state $S blob $(blob $B/states/$S), record $TAG.jsonl blob $(blob $B/states/$TAG.jsonl) ($(grep -c . $B/states/$TAG.jsonl) lines)"
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
bash $K/push_leg127.sh "kc127_leg: the leg ends (exit $rc)" 2>&1 | tail -1 >> $LOGF
tell "macm3 #1025 kc127_leg: the leap ended (exit $rc, wall $(( $(date +%s) - t0 )) s, $(grep -c . $B/pushed_points.txt 2>/dev/null) point(s) pushed: $(tr '\n' ' ' < $B/pushed_points.txt 2>/dev/null)); $([ -e $B/leg_STOP.txt ] && head -1 $B/leg_STOP.txt | cut -c1-200 || echo 'no STOP file'); guard rows: $(tail -n +3 $B/leg_points.txt 2>/dev/null | tr '\n' ' ' | cut -c1-700)"
exit 0
}
