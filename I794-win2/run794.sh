#!/usr/bin/env bash
# #794 on win2: #776's 24-order octo-double series (anm_run.py --save_jet 2, #603's chain_nsr flags) at D 259.5183 and
# 259.5702, 8 threads, from the worktree D:/choptuik-i709 (main 3e096e26) with venv-i600, #603's own build; then the
# records check and its control, Delta's bars (report794.py and its control), and #782's exponents (singularity_type.py
# of origin/main). The bases and #603's records are read from the live clone's I603-win2/chain_nsr, which the chain
# writes; nothing is written there.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I794-win2
WT=/d/choptuik-i709
B=/d/scratch794
mkdir -p $B
cp $RAW/I603-win2/chain_nsr/anm_run.jsonl $B/chain_nsr_records.jsonl
git -C $WT fetch -q origin
git -C $WT show origin/main:hp/singularity_type.py > $B/singularity_type.py
cd $WT/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 8 --corrector od --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred"
echo "hpkernel $("$PY" -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/exits_794.txt
for D in 259.5183 259.5702; do
  cp $RAW/I603-win2/chain_nsr/anm_pin3_D$D.npz $B/anm_pin3_D$D.npz
  t=$(date +%s)
  echo "== D $D $(date -u '+%F %T') UTC" > $R/repro_D$D.log
  "$PY" -u anm_run.py $RAW $R/repro --state $B/anm_pin3_D$D.npz --N 24 --tol_od 1e-60 $CH --save_jet 2 >> $R/repro_D$D.log 2>&1
  echo "D $D exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_794.txt
done
"$PY" -I $R/repro_check794.py $RAW $B/chain_nsr_records.jsonl > $R/repro_check794.txt 2>&1; echo "exit $?" >> $R/repro_check794.txt
"$PY" -I $R/repro_check794.py $RAW $B/chain_nsr_records.jsonl --control > $R/repro_check794_control.txt 2>&1; echo "exit $?" >> $R/repro_check794_control.txt
export PYTHONPATH=$WT/hp
"$PY" $R/report794.py $R/repro/jet_pin3_D*.npz > $R/report794.txt 2>&1; echo "exit $?" >> $R/report794.txt
"$PY" $R/report794.py $R/repro/jet_pin3_D*.npz --mutate=shiftP > $R/report794_shiftP.txt 2>&1; echo "exit $?" >> $R/report794_shiftP.txt
"$PY" $B/singularity_type.py planted > $R/type794_planted.txt 2>&1; echo "exit $?" >> $R/type794_planted.txt
"$PY" $B/singularity_type.py rows $R/repro/jet_pin3_D*.npz --delta > $R/type794.txt 2>&1; echo "exit $?" >> $R/type794.txt
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_794.txt
