#!/bin/bash
# #792 on dh610: #776's 24-order octo-double series (anm_run.py --save_jet 2, #603's chain_nsr flags) at D 259.5502 and
# 259.5901, 4 threads, nice 10, in the worktree choptuik-i608b (a515ab87, which #608 runs; dh610's main checkout a879ccc3
# has no --save_jet) with the main checkout's .venv; then the records check and its control,
# Delta's bars (report792.py and its control), and #782's exponents (singularity_type.py of origin/main). The bases and
# #603's records come from origin/main into ~/scratch792, so the live raw clone is not pulled.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I792-dh610
B=/home/nathan/scratch792
CO=/home/nathan/Source/choptuik-large-d
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I603-win2/chain_nsr/anm_run.jsonl > $B/chain_nsr_records.jsonl
git -C $CO fetch -q origin
git -C $CO show origin/main:hp/singularity_type.py > $B/singularity_type.py
cd /home/nathan/Source/choptuik-i608b/hp && . $CO/.venv/bin/activate
[ "$(git rev-parse --short=8 HEAD)" = "a515ab87" ] || { echo "choptuik-i608b is not at a515ab87" > $R/exits_792.txt; exit 9; }
grep -q save_jet anm_run.py || { echo "anm_run.py has no --save_jet" > $R/exits_792.txt; exit 9; }
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 4 --corrector od --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD), raw origin/main $(git -C $RAW rev-parse --short=8 origin/main)" > $R/exits_792.txt
for D in 259.5502 259.5901; do
  git -C $RAW show origin/main:I603-win2/chain_nsr/anm_pin3_D$D.npz > $B/anm_pin3_D$D.npz
  t=$(date +%s)
  echo "== D $D $(date -u '+%F %T') UTC" > $R/repro_D$D.log
  nice -n 10 python -u anm_run.py $RAW $R/repro --state $B/anm_pin3_D$D.npz --N 24 --tol_od 1e-60 $CH --save_jet 2 >> $R/repro_D$D.log 2>&1
  echo "D $D exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_792.txt
done
python -I $R/repro_check792.py $RAW $B/chain_nsr_records.jsonl > $R/repro_check792.txt 2>&1; echo "exit $?" >> $R/repro_check792.txt
python -I $R/repro_check792.py $RAW $B/chain_nsr_records.jsonl --control > $R/repro_check792_control.txt 2>&1; echo "exit $?" >> $R/repro_check792_control.txt
export PYTHONPATH=/home/nathan/Source/choptuik-i608b/hp
python $R/report792.py $R/repro/jet_pin3_D*.npz > $R/report792.txt 2>&1; echo "exit $?" >> $R/report792.txt
python $R/report792.py $R/repro/jet_pin3_D*.npz --mutate=shiftP > $R/report792_shiftP.txt 2>&1; echo "exit $?" >> $R/report792_shiftP.txt
python $B/singularity_type.py planted > $R/type792_planted.txt 2>&1; echo "exit $?" >> $R/type792_planted.txt
python $B/singularity_type.py rows $R/repro/jet_pin3_D*.npz --delta > $R/type792.txt 2>&1; echo "exit $?" >> $R/type792.txt
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_792.txt
