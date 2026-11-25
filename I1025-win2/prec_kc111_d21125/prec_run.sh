#!/bin/bash
# #1025 prec_kc111_d21125 on win2 (the coordinator's hc of 2026-11-25 ~15:05 UTC): precision check of the hybrid sign near the k_c roots at D 21.125 with d18_hybsign_prec.py (wip/ell1-highD at 18566122, blob a3a1368c):
# (1) dh170's k_c 111 state: lambda 0.860, 0.865, 0.870, 0.875; (2) dh170's k_c 103 state: lambda 0.880, 0.885. One process per lambda, at most 4 at once, at the IDLE priority class (started through
# cim_start_low.ps1) beside the two k_c 95 lanes ("do not slow them"). usage: prec_run.sh   (DRY=1: pins, selftests, the job list; no run)
# Jobs, in order of what decides the question (the four points that straddle the two roots first, the outer k_c 111 points when a slot is free): J1 k_c 111 0.865 | J2 k_c 111 0.870 | J3 k_c 103 0.880 | J4 k_c 103 0.885 | J5 k_c 111 0.860 | J6 k_c 111 0.875.
# Each job: d18_hybsign_prec.py REC STATE 21.125 LAM OUT (noise amplitudes 1e-15, 1e-12, 1e-10, 2 seeds each, and all blocks in double-double: the script's defaults), cap 21600 s (6 h) by the exact root pid (crun);
# a capped job is a stop and is reported. Each finished lambda prints its line (the script's) into prec_k<KC>_lam<LAM>.log and a summary line into summary_prec.txt.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/prec_kc111_d21125; WOUT=D:/choptuik-i935-raw/I1025-win2/prec_kc111_d21125
EX=$OUT/exits_prec.txt; SUM=$OUT/summary_prec.txt
IN=$OUT/inputs; WIN=$WOUT/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter
D=21.125; CAP=21600; MAXP=4
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
mkdir -p $OUT
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "prec D $D refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/d18_hybsign_prec.py a3a1368c "d18_hybsign_prec.py"
chk $IN/kc111/sol_l1kc111dh170h_D21.1250.npy edbb419e "dh170's k_c 111 state"
chk $IN/kc111/l1kc111dh170h.jsonl a0a52e86 "dh170's k_c 111 record"
chk $IN/kc103/sol_l1kc103dh170g_D21.1250.npy ad9b1dc8 "dh170's k_c 103 state"
chk $IN/kc103/l1kc103dh170g.jsonl ac60dbfc "dh170's k_c 103 record"
chk $IN/kc111/dh170_merged_wide_D21.125.jsonl 4bba3f4c "dh170's k_c 111 reference rows"
chk $IN/kc103/dh170_merged_D21.125.jsonl 15feca49 "dh170's k_c 103 reference rows"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "prec D $D refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "prec D $D refuse: solver code differs from 505d8399"; bad=1; }
for f in $OUT/prec_k111_lam0.865.jsonl $OUT/prec_k103_lam0.880.jsonl $OUT/prec_refused.txt $OUT/prec.done; do [ -e $f ] && { log "prec D $D refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
refuse() { log "prec D $D STOP: $*"; echo "prec D $D STOP: $*" >> $SUM; echo "$*" > $OUT/prec_refused.txt; exit ${2:-1}; }
cd $OUT
"$PY" -I $IN/d18_hybsign_prec.py --selftest > selftest_prec.txt 2>&1; q0=$?
"$PY" -I $IN/d18_hybsign_prec.py --selftest --mutate=class > selftest_prec_mutate.txt 2>&1; q1=$?
echo "$q0 $q1" > selftest_exits.txt
[ "$q0 $q1" = "0 1" ] || refuse "the selftests did not behave (prec selftest $q0, mutate=class $q1; wanted 0 1)"
JOBS=("111 0.865" "111 0.870" "103 0.880" "103 0.885" "111 0.860" "111 0.875")
log "prec D $D pins and selftests ok (blobs of the script, states, records and the reference rows; selftest 0, --mutate=class 1); jobs: ${JOBS[*]}; at most $MAXP at once, cap $CAP s each"
[ "$DRY" = 1 ] && { echo "DRY: jobs ${JOBS[*]}"; exit 0; }
cd $WT/solver/matter || exit 1
job() {  # KC LAM
  local K=$1 L=$2 s0=$(date +%s) rc w src rec o lg
  if [ $K = 111 ]; then src=$WIN/kc111/sol_l1kc111dh170h_D21.1250.npy; rec=$WIN/kc111/l1kc111dh170h.jsonl; else src=$WIN/kc103/sol_l1kc103dh170g_D21.1250.npy; rec=$WIN/kc103/l1kc103dh170g.jsonl; fi
  o=$WOUT/prec_k${K}_lam$L.jsonl; lg=$OUT/prec_k${K}_lam$L.log
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $WIN/d18_hybsign_prec.py $rec $src $D $L $o (cwd $WTM, P4_WT_MATTER=$WTM, 1 thread, IDLE class)"; } > $lg
  crun prec_k${K}_$L 0 $CAP d18_hybsign_prec.py "$PY" -u $WIN/d18_hybsign_prec.py $rec $src $D $L $o >> $lg 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $lg
  echo "prec k_c $K lambda $L: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s (a stop)")" >> $SUM
  log "prec_k${K}_$L exit $rc wall $w s capped $CAPPED"
}
running=0
for j in "${JOBS[@]}"; do
  set -- $j
  while [ $running -ge $MAXP ]; do wait -n; running=$((running - 1)); done
  job $1 $2 &
  running=$((running + 1))
  sleep 5
done
wait
cd $OUT
"$PY" -I $IN/../prec_verdict.py $OUT > verdict.txt 2>&1; echo "prec_verdict exit $?" >> verdict.txt
cat verdict.txt >> $SUM
log "prec D $D done: $(tail -n 3 $SUM | cut -c1-200 | tr '\n' ' ')"
touch $OUT/prec.done
exit 0
