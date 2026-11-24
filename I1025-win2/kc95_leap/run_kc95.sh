#!/bin/bash
# #1025 kc95_leap on win2 (the coordinator's hc of 2026-11-24 ~16:20 UTC): "FOR THE FREED THREADS, at tag g's end: a k_c 95 leap, the third resolution along D. Seeds: winb's accepted k_c 95 state at D 21.0 (raw I1025-win/kc95_d21, state d7a4844a,
# record 2e8fe124) and dh170's at D 21.125 (raw I1025-dh170/kc95_d21125); check both with kc95_syscheck_1025.py first (dh610's, controls must exit 1; the kc87 check must refuse them). Command: ell_leap.py l1kc95Lw1025k 1 95 <seed 21.0> 21.0
# <seed 21.125> 21.125 21.75 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold, 4 threads, the same guard (--seeds), 12 h cap, raw kc95_leap/ in your folder, README first. Dry run before the cap so it starts at once. Report each point with the usual row."
# WAITS for all8.done (the tag g leap's end at its cap, 19:19:49 UTC; any end of tag g frees its 4 threads), then: the pins, the seeds (the two states and records, copies in inputs/), kc95_syscheck_1025.py on both (selftest 0, accepts, --mutate=F and
# --mutate=steps exit 1) and kc87_syscheck_1025.py on both (must refuse, exit 1); the guard (leap_guard.py --seeds = the two seed records) and the samplers (launch_kc95_extras.ps1); then the leap, in the k_c 79 worktree (the code of every regrid and
# leap here), 4 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid. usage: run_kc95.sh   (DRY=1: no waiting; the pins, the seed checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc95_leap   # lib_kcl.sh sets OUT to the leap folder
K79=/d/choptuik-i935-raw/I1025-win2/kc79_leap
EX=$OUT/exits_leapk95.txt
SUM=$OUT/summary_leapk95.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc95_leap
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAG=l1kc95Lw1025k
DA=21.0; DB=21.125; H=0.0625; DEND=21.75
SA=$WOUT/inputs/sol_l1kc95winbg_D21.0000.npy; SB=$WOUT/inputs/sol_l1kc95dh170f_D21.1250.npy
RA=$WOUT/inputs/l1kc95winbg.jsonl; RB=$WOUT/inputs/l1kc95dh170f.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leapk95 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
chk $OUT/inputs/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $OUT/inputs/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $OUT/inputs/sol_l1kc95winbg_D21.0000.npy d7a4844a "winb's k_c 95 D 21.0 state"
chk $OUT/inputs/l1kc95winbg.jsonl 4d6ca87d "winb's k_c 95 D 21.0 record (LF form; the CRLF form is blob 2e8fe124)"
chk $OUT/inputs/sol_l1kc95dh170f_D21.1250.npy c9d37744 "dh170's k_c 95 D 21.125 state"
chk $OUT/inputs/l1kc95dh170f.jsonl 6df5a5ee "dh170's k_c 95 D 21.125 record"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leapk95 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leapk95 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $OUT/leapk95.finished $OUT/leapk95.log $OUT/allk95.done $OUT/leapk95_STOP.txt $OUT/leapk95_points.txt $OUT/leapk95_seedA.jsonl $OUT/leapk95_seedB.jsonl; do [ -e $f ] && { log "leapk95 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leapk95 pins checked: ell_leap.py 1eb873e4, leap_guard.py f1fe7c7c, kc95_syscheck d487e628, kc87_syscheck 6df5d960, winb state d7a4844a + record 4d6ca87d, dh170 state c9d37744 + record 6df5a5ee, worktree 48c36355 with solver code = 505d8399"
cd $OUT
"$PY" -I inputs/kc95_syscheck_1025.py --selftest > leapk95_selftest_kc95.txt 2>&1 || { log "leapk95 STOP: kc95_syscheck_1025.py --selftest did not exit 0"; exit 1; }
"$PY" -I inputs/kc87_syscheck_1025.py --selftest > leapk95_selftest_kc87.txt 2>&1 || { log "leapk95 STOP: kc87_syscheck_1025.py --selftest did not exit 0"; exit 1; }
seedcheck() {  # D RECORD STATE TAGNAME
  "$PY" -I inputs/kc95_syscheck_1025.py $2 $3 $1 $WTM > leapk95_syscheck_$4.txt 2>&1 || { log "leapk95 STOP: kc95_syscheck_1025.py does not accept the $4 seed (D $1)"; return 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leapk95_syscheck_$4.txt >> $SUM
  for m in F steps; do "$PY" -I inputs/kc95_syscheck_1025.py $2 $3 $1 $WTM --mutate=$m > leapk95_syscheck_$4_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leapk95 STOP: the control --mutate=$m did not exit 1 on the $4 seed"; return 1; }; done
  "$PY" -I inputs/kc87_syscheck_1025.py $2 $3 $1 $WTM > leapk95_kc87_on_$4.txt 2>&1; [ $? = 1 ] || { log "leapk95 STOP: the kc87 check did not refuse the $4 seed"; return 1; }
  return 0
}
seedcheck $DA $RA $SA winb || exit 1
seedcheck $DB $RB $SB dh170 || exit 1
log "leapk95 seeds accepted by kc95_syscheck_1025.py (D $DA winb, D $DB dh170; selftests 0; --mutate=F and --mutate=steps exit 1; kc87_syscheck_1025.py refuses both)"
CMD="$PY -u ell_leap.py $TAG 1 95 $SA $DA $SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
log "leapk95 waits for the tag g leap's end (all8.done)"
until [ -e $K79/all8.done ]; do sleep 30; done
log "leapk95: the tag g leap has ended ($(tail -n 1 $K79/summary_leap8.txt 2>/dev/null | cut -c1-120)); the seed checks are repeated"
seedcheck $DA $RA $SA winb || exit 1
seedcheck $DB $RB $SB dh170 || exit 1
cp $RA $OUT/leapk95_seedA.jsonl; cp $RB $OUT/leapk95_seedB.jsonl
mkdir -p $OUT/leapk95 $OUT/states
powershell -NoProfile -File $WOUT/launch_kc95_extras.ps1 >> $OUT/leapk95_extras.txt 2>&1
log "leapk95 guard and samplers started (launch_kc95_extras.ps1)"
copier() {
  while [ ! -e $OUT/leapk95.finished ]; do
    for f in $DATA/sol_${TAG}_D*.npy $DATA/sol_${TAG}_last.npy $DATA/sol_${TAG}_prev.npy $DATA/${TAG}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAG}_D*.npy $DATA/sol_${TAG}_last.npy $DATA/sol_${TAG}_prev.npy $DATA/${TAG}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leapk95.log
s0=$(date +%s)
crun leapk95 0 43200 ell_leap.py $CMD >> $OUT/leapk95.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leapk95.log
echo "leapk95: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leapk95.log | tail -n 1)" >> $SUM; log "leapk95 exit $rc wall $w s capped $CAPPED"
touch $OUT/leapk95.finished
wait $cp_pid
echo "kcl leapk95 done" >> $SUM
touch $OUT/allk95.done
exit 0
