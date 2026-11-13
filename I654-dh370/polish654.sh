#!/bin/bash
# #654 step 2: the base polish at the renoded start (x_last 0.975), #603's flags (I603-win2/run_603.sh) with --steps 0 --save_base 1 --tol 1e-30.
# dh370, worktree choptuik-large-d-654 (main 37c7955c) in the venv of choptuik-large-d-614, 12 threads, nice 10.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I654-dh370
cd /home/nathan/Source/choptuik-large-d-654/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
mkdir -p $R/base
echo "== polish $(date -u '+%F %T') UTC, main $(git rev-parse --short=8 HEAD)" > $R/base.log
t=$(date +%s)
nice -n 10 python -u anm_run.py $RAW $R/base --state I654-dh370/start/start_0975.npz --steps 0 --save_base 1 --tol 1e-30 \
   --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 400 --threads 12 --corrector od --tol_od 1e-60 --qd_it 12 \
   --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 >> $R/base.log 2>&1
echo "exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/base.log
