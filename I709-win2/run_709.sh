#!/usr/bin/env bash
# #709: newton_od's natural test with the full step's drop (--od_full_drop / --full_drop 1e-20), on win2.
# Worktree D:/choptuik-i709 at main 0da740e1 or later, venv-i600 (#603's own build, after #523), 8 threads.
#   toy      newton_od_toy.py must pass, and its control --mutate=drop must fail;
#   planted  octo_corrector.py planted at D 200 (T138-win2's state) with --accept natural --full_drop 1e-20, against
#            REF200 (#713's ref_D200), which must hold to 1e-40;
#   A/B      chain_nsr's attempts 4 and 5 (#603: from D 254.0560 at a 0.06628..., and D 254.1222 at a 0.08285..., each
#            7 octo-double steps there), one step each with #603's chain_nsr flags, without (A) and with (B) the option.
# compare_709.py then gives the A/B table: each pair must reach the same D_str and state to 1e-55, B in less corrector
# time than A.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I709-win2
cd /d/choptuik-i709/hp || exit 9
git merge-base --is-ancestor 0da740e1 HEAD || { echo "worktree is older than 0da740e1" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "709 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_709.txt; }
log "start, main $(git rev-parse --short=8 HEAD), hpkernel $("$PY" -c 'import hpkernel; print(hpkernel.__file__)')"
"$PY" -u newton_od_toy.py > $R/toy.log 2>&1
log "toy exit $? (must be 0)"
"$PY" -u newton_od_toy.py --mutate=drop > $R/toy_mutate_drop.log 2>&1
log "toy --mutate=drop exit $? (must be non-zero)"
REF200=1.695088752463841744241523971202762929113
log "planted start"
"$PY" -u octo_corrector.py planted $RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --threads 8 --reseed_o 3 --reseed_start pred --qd 0 \
    --accept natural --full_drop 1e-20 --Delta_ref $REF200 --out $R/planted_D200 > $R/planted_D200.log 2>&1
log "planted exit $? (must be 0)"
NSR="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 8 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
for spec in "att4 I603-win2/chain_nsr/anm_pin3_D254.0560.npz 0.06628036499023438" "att5 I603-win2/chain_nsr/anm_pin3_D254.1222.npz 0.08285045623779297"; do
  set -- $spec
  for side in A B; do
    extra=""; [ $side = B ] && extra="--od_full_drop 1e-20"
    mkdir -p $R/$1_$side
    log "$1_$side start from $2 a0 $3 $extra"
    "$PY" -u anm_run.py $RAW $R/$1_$side --state $2 $NSR --a0 $3 $extra > $R/$1_$side.log 2>&1
    log "$1_$side exit $?"
  done
done
"$PY" -I $R/compare_709.py $R > $R/compare_709.txt 2>&1; log "compare exit $? (must be 0)"
log "all done"
