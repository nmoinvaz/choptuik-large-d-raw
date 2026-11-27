#!/bin/bash
# #1098: D 2000's Moebius ks 3417 (1.5n + 420, set by hand, not gated) measured by ks_gate.py (hp_y/ks_gate_v2.py, the
# copy of wip/large-d-form-s 9e146eff) on its final state (h25, M 48) at kfreeze 23: the octo-double residual's change at
# ks + 200, against the kmax-23 bar 1e-64; fastmul6 site_y, 4 threads; the log beside the run in dh610's raw worktree
{
W=/home/nathan/Source/choptuik-large-d-1088a
T=/home/nathan/Source/choptuik-large-d-raw-1088a/I1098-dh610/fix6/D2000_M48_6b
cp $W/hp_z/ks_gate_v2.py $W/hp_y/ks_gate_v2.py
cd $W/hp_y || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
nice -n 10 $(cat $W/python_path) -u ks_gate_v2.py $T/release_ls_h25_D2000.0000.npz --bar 1e-64 --kfreeze 23 --tries 1 \
  --threads 4 > $W/out/gate2000.log 2>&1
echo "rc $?" >> $W/out/gate2000.log
exit
}
