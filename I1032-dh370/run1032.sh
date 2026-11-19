#!/usr/bin/env bash
# #1032 runner checks on dh370 (Python only, the existing 40f4b4a5 build in ~/Source/choptuik-large-d-961/.venv).
# That build has jacobian_sub but not residual_sub, so res_rows falls back to the full residual with a notice
# (the same bits as before). Run one at a time, nice 10, while the chain is stopped or with --threads 6.
set -u
git -C ~/Source/choptuik-large-d fetch -q origin perf/elim-projections
git -C ~/Source/choptuik-large-d worktree add ~/Source/choptuik-large-d-1032 origin/perf/elim-projections
cd ~/Source/choptuik-large-d-1032/hp || exit 9
PY=~/Source/choptuik-large-d-961/.venv/bin/python
RAW=~/Source/choptuik-large-d-raw-wt613           # any clone that holds I966-dh370/
ST=I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz
OUT=$RAW/I1032-dh370; mkdir -p $OUT               # README.md first line: "# I1032-dh370: ..."
T=10
run() { name=$1; shift; echo "== $name $(date -u '+%F %T')" > $OUT/$name.log; nice -n 10 $PY -u proj_check.py "$@" >> $OUT/$name.log 2>&1; echo "exit $?" >> $OUT/$name.log; }

run mock      mock                                                     # seconds, exit 0
run floor     floor    $RAW $ST --threads $T                           # ~5 min: item 3's diagnostic
run time      time     $RAW $ST --threads $T --rep 2                   # ~30 min: seconds per path and stage
run bits      bits     $RAW $ST --threads $T --plants 0,1e-24          # ~25 min, exit 0
run bits_ulp  bits     $RAW $ST --threads $T --plants 1e-24 --mutate ulp      # ~10 min, must exit 1
run accuracy  accuracy $RAW $ST --threads $T                           # ~30 min, exit 0
run acc_sign  accuracy $RAW $ST --threads $T --plants 1e-24 --mutate sign     # ~12 min, must exit 1
run acc_nobar accuracy $RAW $ST --threads $T --plants 1e-24 --mutate o_nobar  # ~12 min, must exit 1

# The chain A/B: leg 6's first step (D 251.2845 -> 251.8782, a 0.5938 by the rule) with the three flags, against the
# logged step (corrector 3093 s, Delta 1.684652166741953653271185636033235081241, 7 'ladder' projections).
B=I966-dh370/ks_chain3b/leg05_D250.7060_ks293/anm_pin3_D251.2845.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 2e-34 \
--qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
--od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.00715 \
--jet_tangent_from 1 --series_split 1 --a_rise 1 --reseed_qd_bar 1e-13 --ks 293 --keep_plan 0 --D_max 261.2845 --steps 1"
nice -n 10 $PY -u anm_run.py $RAW $OUT/step_new --state $B $F --proj_start pred --reseed_o_stop 1 --proj_o 1 \
  > $OUT/step_new.log 2>&1                                             # ~20-40 min
nice -n 10 $PY -u anm_run.py $RAW $OUT/step_old --state $B $F > $OUT/step_old.log 2>&1   # ~70 min, the same-session control
