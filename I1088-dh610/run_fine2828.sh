#!/bin/bash
# D 2828 on the fine mesh (#1088; form_s_fine.py jump): nodes 0.3 ... 0.7 and from 0.7 to 0.95 with 1 - x times 1 - 4/n,
# the Moebius horizon a = max(8, n/400) = 8 summed at 0.95 (ks 150), kc 250, held; the guess carried from the held
# states at D 1000, 1414 and 2000 along the mesh and fitted at degree 2 in 1/n, Delta the fit's; the sparse float64
# Jacobian (SuperLU) with the octo-double residual, stopped by Delta's first-order bound 1e-15; Track C's
# 1.64755897412515222 +- 1.36e-9 at D 2828 for the comparison; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-buildfine; do sleep 30; done
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'path_s')" || exit 1
bash $W/update_py.sh > /dev/null
test -s $W/hp/form_s_fine.py || exit 1
cd $W/hp || exit 1
mkdir -p $W/out/fine2828
S="$W/out/j1000_held_mob/jump_s_D1000.0000.npz,$W/out/j1414_held_mob/jump_s_D1414.0000.npz,$W/out/j2000_held_mob2/jump_s_D2000.0000.npz"
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $W/out/fine2828/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=4 $(cat $W/python_path) -u form_s_fine.py jump $W/out/fine2828 --D 2828 --states_s "$S" \
  --deg 2 --mob 8 --kc 250 --ks 150 --threads 10 --it_max 10 --tc 1.64755897412515222:1.36e-9 --res od --commit 30d2e0cd \
  --allow_unraw > $W/out/fine2828/fine.log 2>&1
echo "rc $?" >> $W/out/fine2828/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $W/out/fine2828/run.log
exit
}
