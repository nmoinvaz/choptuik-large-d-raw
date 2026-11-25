#!/bin/bash
# D 10000 held at L = 20, x_l 0.706399, ks 13018 (#1088; form_s_lastnode.py solvestate): the guess built on the Mac (I1088-mac-a/form_s/g10000/: the held
# states at D 1000, 1414, 2000, 2200 carried to x_c = 0.707028 and fitted at degree 2; horizon / bulk 5.9), the last node
# at x_c, the Moebius horizon a 24.995 summed there, ks 15017, kc 250, 1372 Taylor steps; the double-double Jacobian and
# the octo-double residual to Delta's bound 1e-15, the quad-double check, the Hamiltonian check; the #1095 refit's
# 1.64493098978 +- 7.5e-10 for the comparison (Track C 1.64493098993 +- 1.7e-9); 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
O=$W/out/L10000
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py solvestate $O --state $W/out/g10000L20/guess_D10000.0000.npz \
  --threads 10 --res dd --delta_tol 1e-15 --tc 1.64493098978:7.5e-10 --commit 91d5bbc5 --allow_unraw > $O/lastnode.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
