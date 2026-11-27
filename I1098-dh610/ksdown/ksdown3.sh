#!/bin/bash
# #1098: the downward ks gate again (ks_gate.py of wip/large-d-form-s 9e146eff or later as hp_z/ks_gate_v2.py: the Delta
# control (moving m_h read 0.0 at this state, all of it and one grid value alike); D 4000 at ks 4717 only (the gate
# of the second run, its control rerun), then D 4628's restarted jump when
# it has converged (from its own ks, steps of 200), fastmul7 site_z, 4 threads; logs into I1098-dh610/ksdown/
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
O=$LV/I1098-dh610/ksdown
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
nice -n 10 $PY -u ks_gate_v2.py $O/jump_s_D4000.0000.npz --bar 1e-64 --down 1 --ks0 4717 --step 100 --ks_min 4717 \
  --threads 4 > $O/D4000_c.log 2>&1
echo "rc $?" >> $O/D4000_c.log
L=$LV/I1098-dh610/ladder/D4628
n=0
until grep -q "^jump ks .* rc 0" $L/run.log 2>/dev/null; do n=$((n + 1)); [ $n -gt 480 ] && exit 2; sleep 30; done
nice -n 10 $PY -u ks_gate_v2.py $L/jump/jump_s_D4628.0000.npz --bar 1e-64 --down 1 --ks_min 3000 --threads 4 > $O/D4628.log 2>&1
echo "rc $?" >> $O/D4628.log
exit
}
