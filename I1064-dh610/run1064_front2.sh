#!/bin/bash
# #1064, the coordinator's front test (21 Nov, comment 7066596082) as amended at 17:40 UTC (comment 7066657942): does the order-293 system's real singularity near D 265.078 move with the order or with the plan?
# At D 262.7908, from leg 14's base, with leg 14's own anm_run.py arguments (dh370's launcher, I966-dh370/ks_chain3b_s_dry.log) except --steps 1 (a single step) and --save_jet 2 (stop once the jet_pin3 file is written; the jet is
# computed as with --save_jet 1), plus --save_base 1 (the saved base carries the run's plan): (a) the control, --ks 293 --keep_plan 1; (b) --ks 293 --keep_plan 0 (if it fails at its first step, that is its result).
# (c), ks 395 at D 262.7908, is NOT run (the amendment: the raise from ks 293 fails at D 262 even for one order). (c') the order arm at D 237.7132: one step each from dh610's ks 307 control base and its ks 395 base, leg 13's arguments
# (the line of the earlier #1064 runs: --tol_od 2e-34, --od_floor_delta 1e-30), --keep_plan 1, --save_jet 2. One after the other, 10 threads, nice 10.
# The control's jet is compared with dh370's (largest relative difference per coefficient, exact), (b) with (a) and the ks 395 jet with the ks 307 jet (information); the plan hashes of the bases are recorded. A run is capped at 14400 s by
# TERM to its exact pid (KILL to it after four more 30 s polls). A run's own wall is the first 30 s poll that finds its pid gone. A braced block ending in exit.
# Env (defaults are the real run): OUT1064F (for a dry test only), CAP1064F.
{
. "$(dirname "$0")/common1064.sh"
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz; S_BLOB=d15cb96c37f580a848328d29c2f69f4d121fc057
JREF=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D262.7908.npz; JREF_BLOB=287f4d70e93e61026bf580573c152be57090677e
B307=I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz; B307_BLOB=861c79ff8ffc4b10067c487287ff46286b4ed4ba
B395=I1064-dh610/ho3_D237.7132/ks395/base_pin3_D237.7132.npz; B395_BLOB=aa072a5e858ec4b04616b21bc10cbeeaca20c3ce
OUT=${OUT1064F:-$SD/front_D262.7908}
mkdir -p $OUT
X=$OUT/exits_front.txt; SUM=$OUT/summary_front.txt
log() { echo "1064 front $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$JREF)" = $JREF_BLOB ] || { log "dh370's jet blob differs from $JREF_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$B307)" = $B307_BLOB ] || { log "the ks 307 base's blob differs from $B307_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$B395)" = $B395_BLOB ] || { log "the ks 395 base's blob differs from $B395_BLOB: stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g i1064j i1064k i1064l i1064m i1064n i1064o i1064p i1064q; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
log "worktree $WT at $M, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), state $S, dh370's jet $JREF"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
. $VENV/bin/activate
cd $OUT
python3 -I $SD/jetdiff1064.py --selftest > jetdiff_selftest.txt 2>&1; j1=$?; python3 -I $SD/jetdiff1064.py --selftest --break > jetdiff_selftest_break.txt 2>&1; j2=$?
python3 -I $SD/planhash1064.py --selftest > planhash_selftest.txt 2>&1; p1=$?; python3 -I $SD/planhash1064.py --selftest --break > planhash_selftest_break.txt 2>&1; p2=$?
python3 -I $SD/jetdiff1064.py $RAW/$JREF $RAW/$JREF > jetdiff_ref_vs_itself.txt 2>&1; j3=$?
echo "controls: jetdiff selftest exit $j1 (0), --break exit $j2 (1), dh370's jet against itself exit $j3 (0); planhash selftest exit $p1 (0), --break exit $p2 (1)" >> $SUM; log "controls jetdiff $j1/$j2/$j3 planhash $p1/$p2"
[ $j1 = 0 ] && [ $j2 = 1 ] && [ $j3 = 0 ] && [ $p1 = 0 ] && [ $p2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
cd $WT/hp || exit 1
# leg 14's arguments (dh370's launcher), --threads 10, --save_jet 2 for --save_jet 1
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 2 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_o_bar 1e-17 --reseed_qd_bar 1e-13 --D_max 271.1415"
# leg 13's arguments for the order arm (the line of the earlier #1064 runs), --save_jet 2 for 1
F13="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 2 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --D_max 270.8483"
CAP=${CAP1064F:-14400}
declare -A RC WALL
go() {  # LABEL STATE K KEEP_PLAN FLAGS JETTAG [SUBDIR]
  local L=$1 ST=$2 K=$3 P=$4 FL=$5 JT=$6 SUB=$7 pid t0 t1 terms=0 capped=
  local D=$OUT${SUB:+/$SUB}
  mkdir -p $D/$L
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1"; } > $D/$L.log
  ( cd $WT/hp && exec nice -n 10 python3 -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1 >> $D/$L.log 2>&1 ) &
  pid=$!; t0=$(date +%s); log "$SUB/$L started (state $ST, ks $K, keep_plan $P), pid $pid"
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
echo "state's own plan (D 262.7908): $(python3 -I $SD/planhash1064.py $RAW/$S)" >> $SUM
echo "ks 307 base's own plan (D 237.7132): $(python3 -I $SD/planhash1064.py $RAW/$B307)" >> $SUM
echo "ks 395 base's own plan (D 237.7132): $(python3 -I $SD/planhash1064.py $RAW/$B395)" >> $SUM
go a_ks293_keepplan1 $S 293 1 "$F" D262.7908
go b_ks293_replan $S 293 0 "$F" D262.7908
go ks307 $B307 307 1 "$F13" D237.7132 order_arm_D237.7132
go ks395 $B395 395 1 "$F13" D237.7132 order_arm_D237.7132
cd $OUT
jd() {  # jd A B TAG
  [ -f $1 ] && [ -f $2 ] || { echo "jetdiff $3: a jet is missing" >> $SUM; return; }
  python3 -I $SD/jetdiff1064.py $1 $2 > jetdiff_$3.txt 2>&1; local rc=$?
  echo "jetdiff $3: exit $rc: $(cat jetdiff_$3.txt)" >> $SUM; log "jetdiff $3 exit $rc"
}
jd $OUT/jet_a_ks293_keepplan1.npz $RAW/$JREF a_vs_dh370      # the control against dh370's jet: the issue's 1e-40 reading
jd $OUT/jet_b_ks293_replan.npz $OUT/jet_a_ks293_keepplan1.npz b_vs_a    # information
jd $OUT/order_arm_D237.7132/jet_ks395.npz $OUT/order_arm_D237.7132/jet_ks307.npz order_arm_ks395_vs_ks307   # information
log "done"
echo "front done" >> $SUM
exit 0
}
