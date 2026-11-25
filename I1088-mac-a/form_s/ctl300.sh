#!/bin/bash
# the controls of form_s.py's stopping rule on Delta's first-order bound (#1088), D 300 held from the guess of the
# octo-double jump I1088-dh370/j300_held (u horizon, degree 3, the 50 chain states), quad-double Jacobian, Mac opt-1
# build, 2 threads: b15 --delta_tol 1e-15 (the default); b30 --delta_tol 1e-30, whose Delta must equal j300_held's
# (tol 1e-40) to 1e-28; s101 --delta_tol 1e-15 with the Jacobian scaled by 1.01, which must not meet the bound in b15's
# number of steps; b30 and s101 take j300_held's Taylor steps (--segs_from); b30h also its held harmonics
# (--held_from), so it solves the same held system as j300_held
{
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a/raw
O=/Users/nathan/Source/choptuik-large-d-raw-1088a/I1088-mac-a/form_s
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp || exit 1
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a/site_m OPENBLAS_NUM_THREADS=2
SF=/Users/nathan/Source/choptuik-large-d-raw-1088a/I1088-dh370/j300_held/jump_s_D300.0000.npz
for v in ${CTL_RUNS:-b15 b30 s101 b30h}; do
  case $v in
    b15) X="--delta_tol 1e-15";;
    b30) X="--delta_tol 1e-30 --segs_from $SF";;
    s101) X="--delta_tol 1e-15 --jscale 1.01 --segs_from $SF";;
    b30h) X="--delta_tol 1e-30 --segs_from $SF --held_from $SF";;
  esac
  mkdir -p $O/ctl300_$v
  nice -n 10 /Users/nathan/venv-314/bin/python -u form_s.py jump $O/ctl300_$v --D 300 \
    --states "$R/I903-macm3/chain_k135/anm_pin3_D*.npz,$R/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz" --Dmin 226 --Dmax 252.5 \
    --deg 3 --kfreeze 13 --plan_tol 1e-40 --ks sigma --tol 1e-300 --it_max 10 --threads 2 --held 1 $X \
    > $O/ctl300_$v/jump.log 2>&1
done
exit
}
