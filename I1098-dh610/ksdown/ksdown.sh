#!/bin/bash
# #1098: the downward ks gate (ks_gate.py of wip/large-d-form-s 99b913c1, as hp_z/ks_gate_v2.py) at bar 1e-64 on D 4000's
# jump state (mm5's, ks 6017, sha256 d542ecda) and then on D 4628's (this machine's live raw worktree, once its jump has
# converged), fastmul7 site_z, 4 threads; each step's change is printed, so the 1e-70 crossing reads off the same run.
# Logs into the live raw worktree's I1098-dh610/ksdown/
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
O=$LV/I1098-dh610/ksdown
mkdir -p $O
cp $W/out/ksdown/jump_s_D4000.0000.npz $O/jump_s_D4000.0000.npz
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
nice -n 10 $PY -u ks_gate_v2.py $O/jump_s_D4000.0000.npz --bar 1e-64 --down 1 --ks_min 3000 --threads 4 > $O/D4000.log 2>&1
echo "rc $?" >> $O/D4000.log
L=$LV/I1098-dh610/ladder/D4628
n=0
until grep -q "^jump ks .* rc 0" $L/run.log 2>/dev/null; do n=$((n + 1)); [ $n -gt 360 ] && exit 2; sleep 30; done
nice -n 10 $PY -u ks_gate_v2.py $L/jump/jump_s_D4628.0000.npz --bar 1e-64 --down 1 --ks_min 3000 --threads 4 > $O/D4628.log 2>&1
echo "rc $?" >> $O/D4628.log
exit
}
