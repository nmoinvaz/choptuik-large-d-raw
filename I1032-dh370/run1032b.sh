#!/usr/bin/env bash
# #1032 follow-up on dh370, at perf/elim-projections 68c0a09f, in a new worktree (the old one may still run step_new)
# (the coordinator's comment 7021253688, both blocks in order, unchanged)
set -u
git -C ~/Source/choptuik-large-d fetch -q origin perf/elim-projections
git -C ~/Source/choptuik-large-d worktree add --detach ~/Source/choptuik-large-d-1032b 68c0a09f
cd ~/Source/choptuik-large-d-1032b/hp || exit 9
PY=~/Source/choptuik-large-d-961/.venv/bin/python
RAW=~/Source/choptuik-large-d-raw-wt613
ST=I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz
OUT=$RAW/I1032-dh370
T=10
run() { name=$1; shift; echo "== $name $(date -u '+%F %T') $(git rev-parse --short HEAD)" > $OUT/$name.log; nice -n 10 $PY -u proj_check.py "$@" >> $OUT/$name.log 2>&1; echo "exit $?" >> $OUT/$name.log; }

run accuracy2  accuracy $RAW $ST --threads $T                          # 25-45 min (probes up to 5 plants), exit 0
PL=$(awk '/^  plant .* default:/ {print $2; exit}' $OUT/accuracy2.log)  # the basin plant accuracy found
[ -n "$PL" ] || { echo "no basin plant in accuracy2.log" >> $OUT/accuracy2.log; exit 2; }
run acc_sign2  accuracy $RAW $ST --threads $T --plants $PL --mutate sign      # ~15 min, must exit 1 (not 2)
run acc_nobar2 accuracy $RAW $ST --threads $T --plants $PL --mutate o_nobar   # ~15 min, must exit 1 (not 2)
run time2      time     $RAW $ST --threads $T --plants $PL --rep 2            # ~25 min, exit 0

B=I966-dh370/ks_chain3b/leg05_D250.7060_ks293/anm_pin3_D251.2845.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 2e-34 \
--qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
--od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.00715 \
--jet_tangent_from 1 --series_split 1 --a_rise 1 --reseed_qd_bar 1e-13 --ks 293 --keep_plan 0 --D_max 261.2845 --steps 1"
nice -n 10 $PY -u anm_run.py $RAW $OUT/step_new2 --state $B $F --proj_start pred --reseed_o_stop 1 --proj_o 1 > $OUT/step_new2.log 2>&1
nice -n 10 $PY -u anm_run.py $RAW $OUT/step_old2 --state $B $F > $OUT/step_old2.log 2>&1
