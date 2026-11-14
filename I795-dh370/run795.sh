#!/bin/bash
# #795 on dh370: #776's series at D 259.2582 and 259.4928 with the plan made at the state (--keep_plan 0, as #686), 12
# threads, nice 10, in #712's worktree choptuik-large-d-685 and the venv of choptuik-large-d-614 (#776's); then
# compare795.py against #776's series, and its control. The bases come from origin/main into ~/scratch795.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I795-dh370
B=/home/nathan/scratch795
mkdir -p $B
git -C $RAW fetch -q origin
git -C /home/nathan/Source/choptuik-large-d fetch -q origin
git -C /home/nathan/Source/choptuik-large-d show origin/main:hp/singularity_type.py > $B/singularity_type.py
for D in 259.2582 259.4928; do mkdir -p $B/I776-dh370/repro; git -C $RAW show origin/main:I776-dh370/repro/jet_pin3_D$D.npz > $B/I776-dh370/repro/jet_pin3_D$D.npz; done
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 12 --corrector od --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/exits_795.txt
for D in 259.2582 259.4928; do
  git -C $RAW show origin/main:I603-win2/chain_nsr/anm_pin3_D$D.npz > $B/anm_pin3_D$D.npz
  t=$(date +%s)
  echo "== D $D $(date -u '+%F %T') UTC" > $R/newplan_D$D.log
  nice -n 10 python -u anm_run.py $RAW $R/newplan --state $B/anm_pin3_D$D.npz --N 24 --tol_od 1e-60 $CH --keep_plan 0 --save_jet 2 >> $R/newplan_D$D.log 2>&1
  echo "D $D exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_795.txt
done
mkdir -p $B/I795-dh370 && ln -sfn $R/newplan $B/I795-dh370/newplan
export PYTHONPATH=$B:/home/nathan/Source/choptuik-large-d-685/hp
python $R/compare795.py $B > $R/compare795.txt 2>&1; echo "exit $?" >> $R/compare795.txt
python $R/compare795.py $B --mutate=shift > $R/compare795_shift.txt 2>&1; echo "exit $?" >> $R/compare795_shift.txt
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_795.txt
