#!/bin/bash
# #1064, the coordinator's thread test of the front control (21 Nov, comment 7067246958): two short runs on the front base at D 262.7908, (a) = leg 14's arguments, --ks 293 --keep_plan 1, --steps 1, --save_jet 2, --save_base 1, 10 threads
# (run1064_front2.sh's first run): (a2) = (a) unchanged, which must equal (a) bit for bit; (a3) = (a) with dh370's launcher environment: dh370's run966s.sh uses --threads 10 (T=10, the same as (a)) and sets no OPENBLAS_NUM_THREADS,
# OMP_NUM_THREADS or MKL_NUM_THREADS (the harnesses here set them to 1), so (a3) unsets them. One after the other, 10 threads, nice 10. Jets: a2 against (a) (bits, and jetdiff), a3 against (a), a3 against dh370's, a2 against dh370's,
# each with the per-order table (jetstats1064.py). A run is capped at 14400 s by TERM to its exact pid. A braced block ending in exit.
# Env (defaults are the real run): OUT1064F (for a dry test only), CAP1064F.
{
. "$(dirname "$0")/common1064.sh"
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz; S_BLOB=d15cb96c37f580a848328d29c2f69f4d121fc057
JREF=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D262.7908.npz; JREF_BLOB=287f4d70e93e61026bf580573c152be57090677e
JA=I1064-dh610/front_D262.7908/jet_a_ks293_keepplan1.npz; JA_SHA=573bf691181b6aef089af20cd45ad8102e7600341b8c12c50e9ee8885f287a10
OUT=${OUT1064F:-$SD/front_D262.7908/thread_test}
mkdir -p $OUT
X=$OUT/exits_front.txt; SUM=$OUT/summary_front.txt
log() { echo "1064 front $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$JREF)" = $JREF_BLOB ] || { log "dh370's jet blob differs from $JREF_BLOB: stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g i1064j i1064k i1064l i1064m i1064n i1064o i1064p i1064q i1064r; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
[ "$(sha256sum $RAW/$JA | cut -d' ' -f1)" = $JA_SHA ] || { log "(a)'s jet differs from the pushed one: stop"; exit 1; }
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), state $S, dh370's jet $JREF, (a)'s jet $JA"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
cd $OUT
python3 -I $SD/jetdiff1064.py --selftest > jetdiff_selftest.txt 2>&1; j1=$?; python3 -I $SD/jetdiff1064.py --selftest --break > jetdiff_selftest_break.txt 2>&1; j2=$?
python3 -I $SD/jetbits1064.py --selftest > jetbits_selftest.txt 2>&1; p1=$?; python3 -I $SD/jetbits1064.py --selftest --break > jetbits_selftest_break.txt 2>&1; p2=$?
python3 -I $SD/jetbits1064.py $RAW/$JA $RAW/$JA > jetbits_a_vs_itself.txt 2>&1; p3=$?
python3 -I $SD/jetdiff1064.py $RAW/$JREF $RAW/$JREF > jetdiff_ref_vs_itself.txt 2>&1; j3=$?
echo "controls: jetdiff selftest exit $j1 (0), --break exit $j2 (1), dh370's jet against itself exit $j3 (0); jetbits selftest exit $p1 (0), --break exit $p2 (1), (a)'s jet against itself exit $p3 (0)" >> $SUM; log "controls jetdiff $j1/$j2/$j3 jetbits $p1/$p2/$p3"
[ $j1 = 0 ] && [ $j2 = 1 ] && [ $j3 = 0 ] && [ $p1 = 0 ] && [ $p2 = 1 ] && [ $p3 = 0 ] || { log "a control is wrong: stop"; exit 1; }
cd $WT/hp || exit 1
# leg 14's arguments (dh370's launcher), --threads 10, --save_jet 2 for --save_jet 1
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 2 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_o_bar 1e-17 --reseed_qd_bar 1e-13 --D_max 271.1415"
# leg 13's arguments for the order arm (the line of the earlier #1064 runs), --save_jet 2 for 1
F13="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 2 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --D_max 270.8483"
CAP=${CAP1064F:-14400}
declare -A RC WALL
go() {  # LABEL STATE K KEEP_PLAN FLAGS JETTAG SUBDIR [ENV PREFIX]
  local L=$1 ST=$2 K=$3 P=$4 FL=$5 JT=$6 SUB=$7 EP=$8 pid t0 t1 terms=0 capped=
  local D=$OUT${SUB:+/$SUB}
  mkdir -p $D/$L
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1"; } > $D/$L.log
  ( cd $WT/hp && exec nice -n 10 $EP python3 -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1 >> $D/$L.log 2>&1 ) &
  pid=$!; t0=$(date +%s); log "$SUB/$L started (state $ST, ks $K, keep_plan $P, env prefix: ${EP:-none}), pid $pid"
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t0 )) -ge $CAP ]; then
      capped=1; terms=$((terms + 1))
      if [ $terms -le 4 ]; then log "$SUB/$L cap $CAP s: TERM to pid $pid"; kill -TERM $pid; else log "$SUB/$L still alive: KILL to pid $pid"; kill -KILL $pid; fi
    fi
    sleep 30
    [ -z "$t1" ] && ! kill -0 $pid 2>/dev/null && t1=$(date +%s)
  done
  [ -z "$t1" ] && t1=$(date +%s)
  wait $pid; RC[$L]=$?; WALL[$L]=$(( t1 - t0 )); echo "exit ${RC[$L]}" >> $D/$L.log
  local J=$D/$L/jet_pin3_$JT.npz
  if [ -f $J ]; then cp $J $D/jet_$L.npz; jh=$(sha256sum $J | cut -c1-16); else jh="no jet"; fi
  echo "${SUB:+$SUB/}$L: state $ST, ks $K, keep_plan $P, exit ${RC[$L]}, own wall ${WALL[$L]} s (30 s polls)${capped:+, capped at $CAP s}; jet $jh" >> $SUM
  log "$SUB/$L exit ${RC[$L]} wall ${WALL[$L]} s jet $jh"
  echo "${SUB:+$SUB/}$L polish/jet lines: $(grep -E 'octo-double Newton|base polish|base re-seed|the base keeps|--ks changes|series saved|no trial step|Traceback|Error' $D/$L.log | cut -c1-220 | tr '\n' '|')" >> $SUM
  B=$(ls $D/$L/base_pin3_D*.npz 2>/dev/null | head -1)
  if [ -n "$B" ]; then echo "${SUB:+$SUB/}$L plan: $(python3 -I $SD/planhash1064.py $B)" >> $SUM; else echo "${SUB:+$SUB/}$L plan: no base saved (the polish was not adopted or did not run)" >> $SUM; fi
}
go a2_unchanged $S 293 1 "$F" D262.7908
go a3_dh370env $S 293 1 "$F" D262.7908 "" "env -u OPENBLAS_NUM_THREADS -u OMP_NUM_THREADS -u MKL_NUM_THREADS"
cd $OUT
jd() {  # jd A B TAG
  [ -f $1 ] && [ -f $2 ] || { echo "jetdiff $3: a jet is missing" >> $SUM; return; }
  python3 -I $SD/jetdiff1064.py $1 $2 > jetdiff_$3.txt 2>&1; local rc=$?
  python3 -I $SD/jetbits1064.py $1 $2 > jetbits_$3.txt 2>&1; local rb=$?
  python3 -I $SD/jetstats1064.py $1 $2 > jetstats_$3.txt 2>&1
  echo "jetdiff $3: exit $rc: $(cat jetdiff_$3.txt); bits: exit $rb: $(cat jetbits_$3.txt)" >> $SUM; log "jetdiff $3 exit $rc bits $rb"
}
JA2=$OUT/jet_a2_unchanged.npz; JA3=$OUT/jet_a3_dh370env.npz
jd $JA2 $RAW/$JA a2_vs_a
jd $JA3 $RAW/$JA a3_vs_a
jd $JA3 $RAW/$JREF a3_vs_dh370
jd $JA2 $RAW/$JREF a2_vs_dh370      # information
jd $RAW/$JA $RAW/$JREF a_vs_dh370_again   # (a) against dh370's, as in the first report
log "done"
echo "thread test done" >> $SUM
exit 0
}
