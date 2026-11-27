#!/bin/bash
# #1101 on win2, R2 ONLY (the coordinator's hc of 2026-11-27 01:44 UTC, after R0 failed its control): kappa 0.35 from the same source state (winb's k_c 127 at D 23.0, blob 7a1b150c), "your driver's R2 line by hand", 6 threads,
# Normal priority (started through cim_start.ps1 -Normal), cap 43200 s on the exact root pid (crun). R1 (kappa 0.5) is skipped. STOP_i1101.txt (R0's failed control) is left on record and not read here.
# After the run: the record, state and log copied into R2/, the kc127 check, and i1101_eval.py --r2 (the amended bar: E = (D0.7 - D0.35) x 16/15 read as real only if |E| >= 2e-6; |E| <= 4e-7 inconclusive).
# usage: run_i1101_r2.sh   (DRY=1: pins, selftests and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw
OUT=$BASE/I1101-win2; WOUT=D:/choptuik-i935-raw/I1101-win2
CHK=$BASE/I1025-win2/kc135_d23/inputs/checks
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc127wind23; TAG=l1kc127k035w2; CAP=43200
export OPENBLAS_NUM_THREADS=6 OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 RAYON_NUM_THREADS=6 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a $OUT/events_i1101.txt; log "i1101 r2 $*"; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) say "refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $DATA/sol_${SRC}_D23.0000.npy 7a1b150c "the source state in the worktree's data/"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/dss_ell.py 5d28c19e "dss_ell.py"
chk $CHK/kc127_syscheck_1025.py 898ebefa "kc127_syscheck_1025.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { say "refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { say "refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/$TAG.jsonl $DATA/sol_${TAG}_D23.0000.npy $OUT/R2/$TAG.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ -s $OUT/R0/l1kc127k070w2.jsonl ] || { say "refuse: R0's record is missing"; bad=1; }
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" -I $OUT/i1101_eval.py --selftest > selftest_eval_r2.txt 2>&1; e0=$?
"$PY" -I $OUT/i1101_eval.py --selftest --mutate > selftest_eval_r2_mutate.txt 2>&1; e1=$?
"$PY" -I $CHK/kc127_syscheck_1025.py --selftest > selftest_kc127_syscheck_r2.txt 2>&1; e2=$?
[ "$e0 $e1 $e2" = "0 1 0" ] || { say "STOP: the selftests did not behave (eval $e0, eval --mutate $e1, kc127 check $e2; wanted 0 1 0)"; exit 3; }
CMD="$PY -u ell_refine.py $SRC 127 $TAG 127 1 23.0 2.0992182200 --kappa 0.35 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
say "R2 pins ok (source 7a1b150c, ell_refine 631e5801, dss_ell 5d28c19e, worktree 48c36355 = solver code 505d8399); evaluator selftest 0 and --mutate 1; kc127 check selftest 0"
[ "${DRY:-0}" = 1 ] && { echo "DRY R2: $CMD"; exit 0; }
mkdir -p $OUT/R2
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 6 threads, Normal priority)"; } > $OUT/R2/lastnode_R2.log
say "R2 starts (kappa 0.35, 6 threads, Normal, cap $CAP s; R1 skipped by the coordinator's ruling)"
s0=$(date +%s)
cd $WT/solver/matter || exit 1
crun R2_i1101 0 $CAP ell_refine.py $CMD >> $OUT/R2/lastnode_R2.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/R2/lastnode_R2.log
say "R2 (kappa 0.35) exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s")"
echo "R2 exit $rc $w" >> $OUT/exits_i1101.txt
if [ -s $DATA/$TAG.jsonl ] && [ -s $DATA/sol_${TAG}_D23.0000.npy ]; then
  cp $DATA/$TAG.jsonl $DATA/sol_${TAG}_D23.0000.npy $OUT/R2/
  "$PY" -I $CHK/kc127_syscheck_1025.py $WOUT/R2/$TAG.jsonl $WOUT/R2/sol_${TAG}_D23.0000.npy 23.0 $WTM > $OUT/R2/syscheck_kc127.txt 2>&1; echo "kc127 check exit $?" >> $OUT/R2/syscheck_kc127.txt
  say "R2 kc127 check: $(tail -n 2 $OUT/R2/syscheck_kc127.txt | tr '\n' ' ' | cut -c1-260)"
fi
"$PY" -I $OUT/i1101_eval.py $OUT --r2 > $OUT/table_r2.txt 2>&1; echo "i1101_eval --r2 exit $?" >> $OUT/table_r2.txt
say "R2 reading: $(grep -E '^bar 2|^amended' $OUT/table_r2.txt | tr '\n' ' ' | cut -c1-500)"
touch $OUT/r2.done
exit 0
