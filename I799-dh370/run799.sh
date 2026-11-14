#!/bin/bash
# #799 on dh370: #776's 24-order octo-double series (anm_run.py --save_jet 2, #603's chain_nsr flags) at D 259.6306 and
# 259.6657, 12 threads, nice 10, in #776's worktree choptuik-large-d-685 and venv; then the records check and its control,
# Delta's bars (report799.py and its control), and #782's exponents (singularity_type.py of origin/main). The bases and
# #603's records come from origin/main into ~/scratch799, so the live raw clone is not pulled.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I799-dh370
B=/home/nathan/scratch799
CO=/home/nathan/Source/choptuik-large-d
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I603-win2/chain_nsr/anm_run.jsonl > $B/chain_nsr_records.jsonl
git -C $CO fetch -q origin
git -C $CO show origin/main:hp/singularity_type.py > $B/singularity_type.py
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 12 --corrector od --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/exits_799.txt
for D in 259.6306 259.6657; do
  git -C $RAW show origin/main:I603-win2/chain_nsr/anm_pin3_D$D.npz > $B/anm_pin3_D$D.npz
  t=$(date +%s)
  echo "== D $D $(date -u '+%F %T') UTC" > $R/repro_D$D.log
  nice -n 10 python -u anm_run.py $RAW $R/repro --state $B/anm_pin3_D$D.npz --N 24 --tol_od 1e-60 $CH --save_jet 2 >> $R/repro_D$D.log 2>&1
  echo "D $D exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_799.txt
done
python -I $R/repro_check799.py $RAW $B/chain_nsr_records.jsonl > $R/repro_check799.txt 2>&1; echo "exit $?" >> $R/repro_check799.txt
python -I $R/repro_check799.py $RAW $B/chain_nsr_records.jsonl --control > $R/repro_check799_control.txt 2>&1; echo "exit $?" >> $R/repro_check799_control.txt
export PYTHONPATH=/home/nathan/Source/choptuik-large-d-685/hp
python $R/report799.py $R/repro/jet_pin3_D*.npz > $R/report799.txt 2>&1; echo "exit $?" >> $R/report799.txt
python $R/report799.py $R/repro/jet_pin3_D*.npz --mutate=shiftP > $R/report799_shiftP.txt 2>&1; echo "exit $?" >> $R/report799_shiftP.txt
python $B/singularity_type.py planted > $R/type799_planted.txt 2>&1; echo "exit $?" >> $R/type799_planted.txt
python $B/singularity_type.py rows $R/repro/jet_pin3_D*.npz --delta > $R/type799.txt 2>&1; echo "exit $?" >> $R/type799.txt
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_799.txt
