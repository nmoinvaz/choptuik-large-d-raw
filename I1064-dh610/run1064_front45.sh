#!/bin/bash
# #1064, the coordinator's order of 21 Nov (~18:55 UTC, comment 7067246958 and its follow-up): (1) (a4): (a) with --threads 5 and with --threads 20, each of which must equal (a) bit for bit (if either does not, report and stop: no (2));
# (2) (a) on dh370's build. dh370's kernel is the hpkernel built from 40f4b4a5 (multishoot 3.3.0, multisolver 0.1.1, multidouble 4.9.0, no Solver.residual_sub); hp/src, Cargo.toml, Cargo.lock, hp/python, pyproject.toml and build.sh are
# identical at 40f4b4a5 and d96a09a1 (git diff empty), so the existing ~/Source/choptuik-large-d-967/.venv (hp/build.sh at d96a09a1 on this machine, avx2, no residual_sub) is that kernel and nothing is built. dh370's python is the
# worktree -966g, stated as 1aa4a4fb (#1032 round 2) in its launcher, but leg 14's --reseed_o_bar came in 268a6b2d (11-20 20:34) and is not in 1aa4a4fb, so its code at leg 14 is not known. Two runs:
# g1 = python of a worktree at 1aa4a4fb (hc's order) with that kernel, leg 14's arguments without --reseed_o_bar (it acts on attempts, not on the jet) and dh370's launcher environment (BLAS variables unset);
# g2 = the python of main 276aa1cd (that of (a)) with that kernel, (a)'s arguments and environment: it differs from (a) in the kernel only.
# Each jet is compared with dh370's and with (a): jetdiff, bits and the per-order table. A run is capped at 14400 s by TERM to its exact pid. A braced block ending in exit.
# Env (defaults are the real run): OUT1064F (for a dry test only), CAP1064F.
{
. "$(dirname "$0")/common1064.sh"
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz; S_BLOB=d15cb96c37f580a848328d29c2f69f4d121fc057
JREF=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D262.7908.npz; JREF_BLOB=287f4d70e93e61026bf580573c152be57090677e
JA=I1064-dh610/front_D262.7908/jet_a_ks293_keepplan1.npz; JA_SHA=573bf691181b6aef089af20cd45ad8102e7600341b8c12c50e9ee8885f287a10
OUT=${OUT1064F:-$SD/front_D262.7908/a4_dh370build}
mkdir -p $OUT
X=$OUT/exits_front.txt; SUM=$OUT/summary_front.txt
log() { echo "1064 front $* $(stamp) UTC" >> $X; }
M=$(git -C $WT rev-parse HEAD) || exit 1
[ "${M:0:8}" = 276aa1cd ] || { log "worktree $WT is at $M, not 276aa1cd: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs from $S_BLOB: stop"; exit 1; }
[ "$(git hash-object $RAW/$JREF)" = $JREF_BLOB ] || { log "dh370's jet blob differs from $JREF_BLOB: stop"; exit 1; }
for u in i1064 i1064b i1064f i1064g i1064j i1064k i1064l i1064m i1064n i1064o i1064p i1064q i1064r i1064s; do [ "$(systemctl --user is-active $u)" != active ] || { log "unit $u still active: stop"; exit 1; }; done
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
go() {  # LABEL STATE K KEEP_PLAN FLAGS JETTAG SUBDIR [ENV PREFIX [PYTHON [WORKTREE]]]
  local L=$1 ST=$2 K=$3 P=$4 FL=$5 JT=$6 SUB=$7 EP=$8 PYB=${9:-python3} WTX=${10:-$WT} pid t0 t1 terms=0 capped=
  local D=$OUT${SUB:+/$SUB}
  mkdir -p $D/$L
  { echo "# $(stamp) UTC worktree $WTX at $(git -C $WTX rev-parse --short HEAD), python $PYB, env prefix ${EP:-none}"; echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1"; } > $D/$L.log
  ( cd $WTX/hp && exec nice -n 10 $EP $PYB -u anm_run.py $RAW $D/$L --state $ST $FL --steps 1 --ks $K --keep_plan $P --save_base 1 >> $D/$L.log 2>&1 ) &
  pid=$!; t0=$(date +%s); log "$SUB/$L started (state $ST, ks $K, keep_plan $P, worktree $WTX, python $PYB, env prefix: ${EP:-none}), pid $pid"
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
FT5=${F/--threads 10/--threads 5}; FT20=${F/--threads 10/--threads 20}
[ "$FT5" != "$F" ] && [ "$FT20" != "$F" ] && [ "${FT5/--threads 5 /}" != "$FT5" ] && [ "${FT20/--threads 20 /}" != "$FT20" ] || { log "the thread flags did not substitute: stop"; exit 1; }
WTG=/home/nathan/Source/choptuik-large-d-1064g; OLDPY=/home/nathan/Source/choptuik-large-d-967/.venv/bin/python
[ "$(git -C $WTG rev-parse HEAD | cut -c1-8)" = 1aa4a4fb ] && [ -z "$(git -C $WTG status --short)" ] || { log "worktree $WTG is not a clean 1aa4a4fb: stop"; exit 1; }
[ -x $OLDPY ] && [ "$($OLDPY -I -c 'import hpkernel; print(hpkernel._hpkernel.Solver is not None and not hasattr(hpkernel._hpkernel.Solver, "residual_sub"))')" = True ] || { log "the old-kernel venv is missing or has residual_sub: stop"; exit 1; }
echo "kernel sources 40f4b4a5 against d96a09a1 (git diff --stat, hp/src hp/Cargo.toml hp/Cargo.lock hp/python hp/pyproject.toml hp/build.sh): '$(git -C /home/nathan/Source/choptuik-large-d diff --stat 40f4b4a5 d96a09a1 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/python hp/pyproject.toml hp/build.sh)' (empty = identical)" >> $SUM
echo "old-kernel venv: $($OLDPY -I -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.isa(), "multidouble", multidouble.isa())'); main venv: $(python3 -I -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.isa(), "multidouble", multidouble.isa())')" >> $SUM
go a4_threads5 $S 293 1 "$FT5" D262.7908
go a4_threads20 $S 293 1 "$FT20" D262.7908
cd $OUT
jd() {  # jd A B TAG
  [ -f $1 ] && [ -f $2 ] || { echo "jetdiff $3: a jet is missing" >> $SUM; return; }
  python3 -I $SD/jetdiff1064.py $1 $2 > jetdiff_$3.txt 2>&1; local rc=$?
  python3 -I $SD/jetbits1064.py $1 $2 > jetbits_$3.txt 2>&1; local rb=$?
  python3 -I $SD/jetstats1064.py $1 $2 > jetstats_$3.txt 2>&1
  echo "jetdiff $3: exit $rc: $(cat jetdiff_$3.txt); bits: exit $rb: $(cat jetbits_$3.txt)" >> $SUM; log "jetdiff $3 exit $rc bits $rb"
}
JA4A=$OUT/jet_a4_threads5.npz; JA4B=$OUT/jet_a4_threads20.npz
jd $JA4A $RAW/$JA a4_threads5_vs_a
jd $JA4B $RAW/$JA a4_threads20_vs_a
if python3 -I $SD/jetbits1064.py $JA4A $RAW/$JA > /dev/null 2>&1 && python3 -I $SD/jetbits1064.py $JA4B $RAW/$JA > /dev/null 2>&1; then
  echo "(a4) gate: both identical to (a) bit for bit: (2) runs" >> $SUM; log "a4 gate passed"
else
  echo "(a4) gate FAILED: a thread count changed the jet: report and stop, (2) not run" >> $SUM; log "a4 gate FAILED: (2) not run, done"; log "done"; echo "front a4 done (gate failed)" >> $SUM; exit 0
fi
FG=${F/ --reseed_o_bar 1e-17/}
[ "$FG" != "$F" ] || { log "--reseed_o_bar did not drop from the leg 14 line: stop"; exit 1; }
cd $WT/hp
go g1_py1aa4a4fb_oldkernel $S 293 1 "$FG" D262.7908 "" "env -u OPENBLAS_NUM_THREADS -u OMP_NUM_THREADS -u MKL_NUM_THREADS" $OLDPY $WTG
go g2_py276aa1cd_oldkernel $S 293 1 "$F" D262.7908 "" "" $OLDPY $WT
cd $OUT
JG1=$OUT/jet_g1_py1aa4a4fb_oldkernel.npz; JG2=$OUT/jet_g2_py276aa1cd_oldkernel.npz
jd $JG1 $RAW/$JREF g1_vs_dh370
jd $JG2 $RAW/$JREF g2_vs_dh370
jd $JG1 $RAW/$JA g1_vs_a
jd $JG2 $RAW/$JA g2_vs_a
jd $RAW/$JA $RAW/$JREF a_vs_dh370_again   # (a) against dh370's, as in the first report
log "done"
echo "front a4 and dh370 build done" >> $SUM
exit 0
}
