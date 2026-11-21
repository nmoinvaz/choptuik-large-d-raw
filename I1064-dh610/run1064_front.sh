#!/bin/bash
# #1064, the coordinator's front test (21 Nov, comment 7066596082): does the order-293 system's real singularity near D 265.078 move with the order or with the plan? Three single steps from leg 14's base at D 262.7908,
# each with leg 14's own anm_run.py arguments (dh370's launcher, I966-dh370/ks_chain3b_s_dry.log) except --steps 1 (a single step) and --save_jet 2 (stop once the jet_pin3 file is written; the jet is computed as with --save_jet 1),
# plus --save_base 1 (the saved base carries the run's plan): (a) the control, --ks 293 --keep_plan 1; (b) --ks 293 --keep_plan 0; (c) --ks 395 (it re-plans; --keep_plan 0 as leg 14's). One after the other, 10 threads, nice 10.
# The control's jet is compared with dh370's (largest relative difference per coefficient, exact), (b) with (a) and (c) with (b) (information), and the plan hashes of the bases are recorded. A run is capped at 14400 s by TERM to its exact pid
# (KILL to it after four more 30 s polls). A run's own wall is the first 30 s poll that finds its pid gone. A braced block ending in exit.
# Env (defaults are the real run): OUT1064F (for a dry test only), CAP1064F.
{
. "$(dirname "$0")/common1064.sh"
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz; S_BLOB=d15cb96c37f580a848328d29c2f69f4d121fc057
JREF=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D262.7908.npz; JREF_BLOB=287f4d70e93e61026bf580573c152be57090677e
OUT=${OUT1064F:-$SD/front_D262.7908}
mkdir -p $OUT
X=$OUT/exits_front.txt; SUM=$OUT/summary_front.txt
log() { echo "1064 front $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$JREF)" = $JREF_BLOB ] || { log "dh370's jet blob differs from $JREF_BLOB: stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g i1064j i1064k i1064l i1064m i1064n i1064o i1064p; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
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
CAP=${CAP1064F:-14400}
declare -A RC WALL
go() {  # LABEL K KEEP_PLAN
  local L=$1 K=$2 P=$3 pid t0 t1 terms=0 capped=
  mkdir -p $OUT/$L
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/$L --state $S $F --steps 1 --ks $K --keep_plan $P --save_base 1"; } > $OUT/$L.log
  ( cd $WT/hp && exec nice -n 10 python3 -u anm_run.py $RAW $OUT/$L --state $S $F --steps 1 --ks $K --keep_plan $P --save_base 1 >> $OUT/$L.log 2>&1 ) &
  pid=$!; t0=$(date +%s); log "$L started (ks $K, keep_plan $P), pid $pid"
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t0 )) -ge $CAP ]; then
      capped=1; terms=$((terms + 1))
      if [ $terms -le 4 ]; then log "$L cap $CAP s: TERM to pid $pid"; kill -TERM $pid; else log "$L still alive: KILL to pid $pid"; kill -KILL $pid; fi
    fi
    sleep 30
    [ -z "$t1" ] && ! kill -0 $pid 2>/dev/null && t1=$(date +%s)
  done
  [ -z "$t1" ] && t1=$(date +%s)
  wait $pid; RC[$L]=$?; WALL[$L]=$(( t1 - t0 )); echo "exit ${RC[$L]}" >> $OUT/$L.log
  local J=$OUT/$L/jet_pin3_D262.7908.npz
  if [ -f $J ]; then cp $J $OUT/jet_$L.npz; jh=$(sha256sum $J | cut -c1-16); else jh="no jet"; fi
  echo "$L: ks $K, keep_plan $P, exit ${RC[$L]}, own wall ${WALL[$L]} s (30 s polls)${capped:+, capped at $CAP s}; jet $jh" >> $SUM
  log "$L exit ${RC[$L]} wall ${WALL[$L]} s jet $jh"
  echo "$L re-seed/polish: $(grep -E 'octo-double Newton|base polish|base re-seed|the base keeps|--ks changes|series saved' $OUT/$L.log | cut -c1-220 | tr '\n' '|')" >> $SUM
  B=$(ls $OUT/$L/base_pin3_D*.npz 2>/dev/null | head -1)
  if [ -n "$B" ]; then echo "$L plan: $(python3 -I $SD/planhash1064.py $B)" >> $SUM; else echo "$L plan: no base saved (the polish was not adopted or did not run)" >> $SUM; fi
}
echo "state's own plan: $(python3 -I $SD/planhash1064.py $RAW/$S)" >> $SUM
go a_ks293_keepplan1 293 1
go b_ks293_replan 293 0
go c_ks395 395 0
cd $OUT
jd() {  # jd A B TAG
  [ -f $1 ] && [ -f $2 ] || { echo "jetdiff $3: a jet is missing" >> $SUM; return; }
  python3 -I $SD/jetdiff1064.py $1 $2 > jetdiff_$3.txt 2>&1; local rc=$?
  echo "jetdiff $3: exit $rc: $(cat jetdiff_$3.txt)" >> $SUM; log "jetdiff $3 exit $rc"
}
jd $OUT/jet_a_ks293_keepplan1.npz $RAW/$JREF a_vs_dh370      # the control against dh370's jet: the issue's 1e-40 reading
jd $OUT/jet_b_ks293_replan.npz $OUT/jet_a_ks293_keepplan1.npz b_vs_a    # information
jd $OUT/jet_c_ks395.npz $OUT/jet_b_ks293_replan.npz c_vs_b            # information
log "done"
echo "front done" >> $SUM
exit 0
}
