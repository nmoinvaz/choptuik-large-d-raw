#!/bin/bash
# #784 on dh610 (the second A/B): newton_od's abort_theta on #608's step from D 249.5375 (chain d6, restart2) with the
# step forced to #608's a 0.48828125 (--a0), on #608's own build (the main checkout's .venv, a879ccc3): A with #608's flags,
# B with --od_abort_theta 1e8 added, one step each from the same base (--steps 1), 4 threads (beside #608), nice 10, in the worktree
# choptuik-large-d-784 at main fdfc5dfa or later. In #608 the attempt at a 0.4883 crawled to
# the 20-step limit and the retry at a 0.2441 converged; A must reproduce that, B refuse a 0.4883 at iteration 1.
# The base comes from origin/main into ~/scratch784, so the live raw clone is not pulled.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I784-dh610
B=/home/nathan/scratch784
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I608-dh610/restart2_d6/anm_pin3_D249.5375.npz > $B/anm_pin3_D249.5375.npz
cd /home/nathan/Source/choptuik-large-d-784/hp && . /home/nathan/Source/choptuik-large-d/.venv/bin/activate
git merge-base --is-ancestor fdfc5dfa HEAD || { echo "worktree is older than fdfc5dfa" > $R/exits_784.txt; exit 9; }
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
F608="--kfreeze 3 --held_fit data/held_fit_d6.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 254 --threads 4 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --a0 0.48828125"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/exits_784.txt
for side in A B; do
  extra=""; [ $side = B ] && extra="--od_abort_theta 1e8"
  t=$(date +%s)
  echo "== $side $(date -u '+%F %T') UTC $extra" > $R/$side.log
  nice -n 10 python -u anm_run.py $RAW $R/$side --state $B/anm_pin3_D249.5375.npz $F608 $extra >> $R/$side.log 2>&1
  echo "$side exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_784.txt
done
python -I $R/compare784.py $R > $R/compare784.txt 2>&1; echo "exit $?" >> $R/compare784.txt
python -I $R/compare784.py --selftest > $R/compare784_selftest.txt 2>&1; echo "exit $?" >> $R/compare784_selftest.txt
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_784.txt
