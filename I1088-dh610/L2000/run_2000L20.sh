#!/bin/bash
# D 2000 held at L = 20 (#1088; form_s_lastnode.py solvestate at 96b6ddc9), the start of its release: the guess of
# out/g2000L20 (built on the Mac, I1088-mac-a/form_s/g2000L20/: the held states at D 1000, 1414, 2200 carried to
# x_l 0.703559 and fitted at degree 2), a 8, ks 2618, kc 250, 304 Taylor steps; the precision ladder (up to 4
# double-double steps, then up to 2 with the quad-double residual; double-double Jacobian) to Delta's bound 1e-15, each
# step's state saved; the check one precision up, the Hamiltonian check; Track C 1.649074313886 +- 1.2e-9; 4 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "def newton_ladder" $W/hp/form_s.py || exit 1
O=$W/out/L2000
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py solvestate $O --state $W/out/g2000L20/guess_D2000.0000.npz \
  --threads 4 --ladder dd,qd --it_max 4 --it_hi 2 --delta_tol 1e-15 --tc 1.649074313886:1.2e-9 --commit 96b6ddc9 --allow_unraw > $O/lastnode.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
