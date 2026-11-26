#!/bin/bash
# #1025 prec_k103_cheap on win2 (the coordinator's hc of 2026-11-26 ~00:59 UTC): the cheapest precision check of the hybrid sign beside the k_c 103 root at D 21.125 with d18_hybsign_prec.py
# (blob a3a1368c), --noise=1e-12,1e-10 --alldd=0; lambda 0.880 and 0.885, one process each, cap 14 h (50400 s) each by the exact root pid (crun), BelowNormal (started through cim_start.ps1).
# usage: run_prec_cheap.sh   (DRY=1: pins and selftests only, no run)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/prec_k103_cheap; WOUT=D:/choptuik-i935-raw/I1025-win2/prec_k103_cheap
EX=$OUT/exits_prec.txt; SUM=$OUT/summary_prec.txt
IN=$OUT/inputs; WIN=$WOUT/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
D=21.125; CAP=50400
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "prec103 D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign_prec.py a3a1368c "d18_hybsign_prec.py"
chk $IN/kc103/sol_l1kc103dh170g_D21.1250.npy ad9b1dc8 "dh170's k_c 103 state"
chk $IN/kc103/l1kc103dh170g.jsonl ac60dbfc "dh170's k_c 103 record"
chk $IN/kc103/dh170_merged_D21.125.jsonl 15feca49 "dh170's k_c 103 reference rows"
chk $OUT/prec_verdict.py d881adf0 "prec_verdict.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "prec103 D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "prec103 D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/prec_k103_lam0.880.jsonl $OUT/prec_k103_lam0.885.jsonl $OUT/prec_refused.txt $OUT/prec.done; do [ -e $f ] && { log "prec103 D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "prec103 D $D STOP: $*"; echo "prec103 D $D STOP: $*" >> $SUM; echo "$*" > $OUT/prec_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/d18_hybsign_prec.py --selftest > selftest_prec.txt 2>&1; q0=$?
"$PY" -I $IN/d18_hybsign_prec.py --selftest --mutate=class > selftest_prec_mutate.txt 2>&1; q1=$?
"$PY" -I $OUT/prec_verdict.py --selftest > selftest_verdict.txt 2>&1; q2=$?
"$PY" -I $OUT/prec_verdict.py --selftest --mutate > selftest_verdict_mutate.txt 2>&1; q3=$?
echo "$q0 $q1 $q2 $q3" > selftest_exits.txt
[ "$q0 $q1 $q2 $q3" = "0 1 0 1" ] || refuse "the selftests did not behave (prec $q0, prec mutate=class $q1, verdict $q2, verdict mutate $q3; wanted 0 1 0 1)"
log "prec103 D $D pins and selftests ok (selftests 0 1 0 1); jobs: k_c 103 lambda 0.880 and 0.885, cap $CAP s each"
[ "$DRY" = 1 ] && { echo "DRY: pins and selftests ok"; exit 0; }
cd $WT/solver/matter || exit 1
job() {  # LAM
  local L=$1 s0=$(date +%s) rc src rec o lg
  src=$WIN/kc103/sol_l1kc103dh170g_D21.1250.npy; rec=$WIN/kc103/l1kc103dh170g.jsonl
  o=$WOUT/prec_k103_lam$L.jsonl; lg=$OUT/prec_k103_lam$L.log
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign_prec.py $rec $src $D $L $o --noise=1e-12,1e-10 --alldd=0 (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread, BelowNormal)"; } > $lg
  crun prec103_$L 0 $CAP d18_hybsign_prec.py "$PY" -u $WIN/d18_hybsign_prec.py $rec $src $D $L $o --noise=1e-12,1e-10 --alldd=0 >> $lg 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $lg
  echo "prec k_c 103 lambda $L: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s (a stop)")" >> $SUM
  log "prec103_$L exit $rc wall $w s capped $CAPPED"
}
job 0.880 &
sleep 5
job 0.885 &
wait
cd $OUT
"$PY" -I $OUT/prec_verdict.py $OUT > verdict.txt 2>&1; echo "prec_verdict exit $?" >> verdict.txt
cat verdict.txt >> $SUM
log "prec103 D $D done: $(tail -n 3 $SUM | cut -c1-200 | tr '\n' ' ')"
touch $OUT/prec.done
exit 0
