#!/bin/bash
# #1101 on win2 (the coordinator's hc of 2026-11-26 20:31 UTC): the accepted k_c 127 state at D 23.0 (winb's, blob 7a1b150c) re-solved at the same k_c with kappa 0.7 (R0, the control), then 0.5 and 0.35 (R1, R2 together).
# ell_refine.py in D:\choptuik-i1025k79 (48c36355), 6 threads each (OPENBLAS/OMP/MKL/RAYON), Normal priority (started through cim_start.ps1 -Normal), cap 43200 s on the exact root pid (crun), no retry.
# R0 first, alone; its control (i1101_eval.py --control) must pass before R1 and R2 start; if it fails the driver stops (STOP_R0.txt) and nothing else runs.
# usage: run_i1101.sh   (DRY=1: pins, selftests, the commands; no run)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw
OUT=$BASE/I1101-win2; WOUT=D:/choptuik-i935-raw/I1101-win2
CHK=$BASE/I1025-win2/kc135_d23/inputs/checks; WCHK=D:/choptuik-i935-raw/I1025-win2/kc135_d23/inputs/checks
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc127wind23; CAP=43200
export OPENBLAS_NUM_THREADS=6 OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 RAYON_NUM_THREADS=6 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a $OUT/events_i1101.txt; log "i1101 $*"; }
refuse() { say "STOP: $*"; echo "$*" > $OUT/STOP_i1101.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) say "refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $DATA/sol_${SRC}_D23.0000.npy 7a1b150c "the source state in the worktree's data/"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/dss_ell.py 5d28c19e "dss_ell.py"
chk $CHK/kc127_syscheck_1025.py 898ebefa "kc127_syscheck_1025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { say "refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { say "refuse: solver code differs from 505d8399"; bad=1; }
for t in l1kc127k070w2 l1kc127k050w2 l1kc127k035w2; do for f in $DATA/$t.jsonl $DATA/sol_${t}_D23.0000.npy; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done; done
[ -e $OUT/STOP_i1101.txt ] && { say "refuse: STOP_i1101.txt exists"; bad=1; }
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" -I $OUT/i1101_eval.py --selftest > selftest_eval.txt 2>&1; e0=$?
"$PY" -I $OUT/i1101_eval.py --selftest --mutate > selftest_eval_mutate.txt 2>&1; e1=$?
"$PY" -I $CHK/kc127_syscheck_1025.py --selftest > selftest_kc127_syscheck.txt 2>&1; e2=$?
[ "$e0 $e1 $e2" = "0 1 0" ] || refuse "the selftests did not behave (eval $e0, eval --mutate $e1, kc127 check $e2; wanted 0 1 0)"
say "pins ok (source state 7a1b150c, ell_refine 631e5801, dss_ell 5d28c19e, worktree 48c36355 = solver code 505d8399); selftests 0 1 0"
mk() { echo "$PY -u ell_refine.py $SRC 127 $1 127 1 23.0 2.0992182200 --kappa $2 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"; }
[ "$DRY" = 1 ] && { echo "DRY R0: $(mk l1kc127k070w2 0.7)"; echo "DRY R1: $(mk l1kc127k050w2 0.5)"; echo "DRY R2: $(mk l1kc127k035w2 0.35)"; exit 0; }
run() {  # NAME TAG KAPPA
  local N=$1 T=$2 K=$3 s0=$(date +%s) rc w CMD
  CMD=$(mk $T $K)
  mkdir -p $OUT/$N
  { echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 6 threads, Normal priority)"; } > $OUT/$N/lastnode_$N.log
  cd $WT/solver/matter || exit 1
  crun ${N}_i1101 0 $CAP ell_refine.py $CMD >> $OUT/$N/lastnode_$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/$N/lastnode_$N.log
  say "$N (kappa $K) exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s")"
  echo "$N exit $rc $w" >> $OUT/exits_i1101.txt
  if [ -s $DATA/$T.jsonl ] && [ -s $DATA/sol_${T}_D23.0000.npy ]; then
    cp $DATA/$T.jsonl $DATA/sol_${T}_D23.0000.npy $OUT/$N/
    "$PY" -I $CHK/kc127_syscheck_1025.py $WOUT/$N/$T.jsonl $WOUT/$N/sol_${T}_D23.0000.npy 23.0 $WTM > $OUT/$N/syscheck_kc127.txt 2>&1; echo "kc127 check exit $?" >> $OUT/$N/syscheck_kc127.txt
    say "$N kc127 check: $(tail -n 2 $OUT/$N/syscheck_kc127.txt | tr '\n' ' ' | cut -c1-260)"
  fi
}
say "R0 starts (kappa 0.7, alone)"
run R0 l1kc127k070w2 0.7
"$PY" -I $OUT/i1101_eval.py $OUT --control > $OUT/R0_control.txt 2>&1; c=$?
say "R0 control: $(cat $OUT/R0_control.txt | tr '\n' ' ' | cut -c1-300) (exit $c)"
[ $c = 0 ] || refuse "R0 fails its control (exit $c): R1 and R2 are not started; report to the coordinator" 3
say "R0 passed its control; R1 (kappa 0.5) and R2 (kappa 0.35) start together"
run R1 l1kc127k050w2 0.5 &
sleep 20
run R2 l1kc127k035w2 0.35 &
wait
"$PY" -I $OUT/i1101_eval.py $OUT > $OUT/table.txt 2>&1; echo "i1101_eval exit $?" >> $OUT/table.txt
say "all three done: see table.txt: $(grep -E '^bar|^R' $OUT/table.txt | head -12 | tr '\n' ' ' | cut -c1-400)"
touch $OUT/i1101.done
exit 0
