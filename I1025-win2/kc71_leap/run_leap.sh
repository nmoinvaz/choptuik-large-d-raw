#!/bin/bash
# #1025 kc71_leap on win2 (the coordinator's hc of 2026-11-22 ~03:00 UTC): carry lambda_1 on to D 20 at k_c 71. Part 1: make the second seed (D 18.4375, k_c 71) the way the D 18.5 state was made: regrid the k_c 63 leap state there
# (I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy, blob 16a17e5f) to k_c 71 with ell_refine.py --no-gamma, accept it by kc71_syscheck.py (the record class's |F| <= 1e-9, the saved state reproducing its record: the step count and |F| come back,
# two controls), then leap the D 18.4375 and D 18.5 (kc71_d185) k_c 71 states to D 20 with ell_leap.py and winb's flags (I1025-win/leap_kc63.log header: --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold), h 0.0625, 4 BLAS threads,
# BelowNormal (the caller sets it), cap 43200 s (12 h) by the exact root pid. Every state is saved (ell_leap.py's own saves) and copied into states/ by a copier loop; the record data/l1kc71Lw1025.jsonl too.
# A regrid that does not converge, or a leap that stops, is reported as it is (no retry).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
DATA=$WT/solver/matter/data
TAGR=l1kc71Wm1025
TAGL=l1kc71Lw1025
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/sol_l1kc63Wm1025_D18.4375.npy 16a17e5f "the k_c 63 D 18.4375 state (inputs copy)"
chk /d/choptuik-large-d-raw-push/I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy 16a17e5f "the k_c 63 D 18.4375 state (raw)"
chk $DATA/sol_${TAGR}_D18.5000.npy 28bf6bac "the k_c 71 D 18.5 state (worktree data)"
chk $OUT/../kc71_d185/sol_l1kc71Wm1025_D18.5000.npy 28bf6bac "the k_c 71 D 18.5 state (kc71_d185 raw)"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_leap.py "" "ell_leap.py (recorded)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/sol_${TAGR}_D18.4375.npy $DATA/${TAGL}.jsonl; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "pins checked: the k_c 63 D 18.4375 state 16a17e5f, the k_c 71 D 18.5 state 28bf6bac, ell_refine.py 631e5801, ell_leap.py $(git hash-object $WT/solver/matter/ell_leap.py | cut -c1-8), worktree 48c36355 with solver code = 505d8399, venv-md510"
cd $OUT
"$PY" kc71_syscheck.py --selftest > selftest_syscheck.txt 2>&1; s1=$?
echo "controls: kc71_syscheck selftest $s1 (0)" >> $SUM; log "controls $s1"
[ $s1 = 0 ] || { log "a control is wrong: stop"; exit 1; }
# ---- part 1a: the second seed, D 18.4375 at k_c 71
cp $OUT/inputs/sol_l1kc63Wm1025_D18.4375.npy $DATA/sol_l1kc63Wm1025_D18.4375.npy
chk $DATA/sol_l1kc63Wm1025_D18.4375.npy 16a17e5f "the state copied into the worktree"
[ $bad = 0 ] || exit 2
LAM0=2.1184454184
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $PY -u ell_refine.py l1kc63Wm1025 63 $TAGR 71 1 18.4375 $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd $WTM, 4 threads)"; } > $OUT/regrid_D18.4375.log
s0=$(date +%s)
crun regrid 0 21600 ell_refine.py "$PY" -u ell_refine.py l1kc63Wm1025 63 $TAGR 71 1 18.4375 $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma >> $OUT/regrid_D18.4375.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid_D18.4375.log
echo "regrid D 18.4375: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "regrid exit $rc wall $w s capped $CAPPED"
stop() { echo "$1" >> $SUM; log "$1"; echo "kcl stopped before the leap" >> $SUM; touch $OUT/all.done; exit 0; }
[ $rc = 0 ] || stop "the D 18.4375 regrid did not finish (exit $rc): the task stops with a report; no leap starts"
[ -s data/sol_${TAGR}_D18.4375.npy ] || stop "the D 18.4375 regrid wrote no state: the task stops with a report; no leap starts"
cp data/sol_${TAGR}_D18.4375.npy data/${TAGR}.jsonl $OUT/states/
cd $OUT
s0=$(date +%s)
"$PY" kc71_syscheck.py $WOUT/states/${TAGR}.jsonl $WOUT/states/sol_${TAGR}_D18.4375.npy 18.4375 $WTM > syscheck_D18.4375.txt 2>&1; ac=$?
echo "acceptance check D 18.4375: exit $ac, $(( $(date +%s) - s0 )) s: $(grep -E '^(ACCEPTED|NOT ACCEPTED)' syscheck_D18.4375.txt)" >> $SUM; log "acceptance exit $ac"
[ $ac = 0 ] || stop "the D 18.4375 state is not accepted ($(grep -E '^NOT ACCEPTED' syscheck_D18.4375.txt | cut -c1-200)): the task stops with a report; no leap starts"
# ---- part 1b: the leap
copier() { # copies new saved states and the record into states/ every 120 s (a file only when it is at least 30 s old)
  while [ ! -e $OUT/leap.finished ]; do
    for f in $DATA/sol_${TAGL}_D*.npy $DATA/sol_${TAGL}_last.npy $DATA/sol_${TAGL}_prev.npy $DATA/${TAGL}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAGL}_D*.npy $DATA/sol_${TAGL}_last.npy $DATA/sol_${TAGL}_prev.npy $DATA/${TAGL}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $PY -u ell_leap.py $TAGL 1 71 data/sol_${TAGR}_D18.4375.npy 18.4375 data/sol_${TAGR}_D18.5000.npy 18.5 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold (cwd $WTM, 4 threads)"; } > $OUT/leap.log
s0=$(date +%s)
crun leap 0 43200 ell_leap.py "$PY" -u ell_leap.py $TAGL 1 71 data/sol_${TAGR}_D18.4375.npy 18.4375 data/sol_${TAGR}_D18.5000.npy 18.5 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold >> $OUT/leap.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap.log
echo "leap: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap.log | tail -n 1)" >> $SUM; log "leap exit $rc wall $w s capped $CAPPED"
touch $OUT/leap.finished
wait $cp_pid
cd $OUT
"$PY" leap_report.py $WOUT > leap_report.md 2>&1
echo "leap_report: exit $?" >> $SUM
log "done"; echo "kcl leap done" >> $SUM
touch $OUT/all.done
exit 0
