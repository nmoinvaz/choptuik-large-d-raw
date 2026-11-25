#!/bin/bash
# D 5656.8542 held (x_l 0.705855, a 14.137, ks 7372; guess from D 2200, 2828.4271, 4000; Track C 1.64572696728365737 +- 1.59e-9). Template: D 2828.4271 held with the last node at L = ln F = 20 (#1088; x_l = 1/sqrt(1 + e^(2L/n)) = 0.704601, the refactor
# subagent's choice: the basin at x_c's side, Delta's gain near the old D 1000's): the guess built on the Mac
# (I1088-mac-a/form_s/g2828L20/, from the held states at D 1414, 2000, 2200, degree 2; horizon block 1.8e-8), the Moebius
# horizon a 8, ks 3700 (1.3 n + 20), kc 250; the double-double Jacobian and residual to Delta's bound 1e-15, the
# quad-double check, the Hamiltonian check; the #1095 refit 1.64755842103839 +- 5.7e-10; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
bash $W/update_py.sh > /dev/null
grep -q "solvestate" $W/hp/form_s_lastnode.py || exit 1
cd $W/hp || exit 1
O=$W/out/L5657
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py solvestate $O --state $W/out/g5657L20/guess_D5656.8542.npz \
  --threads 6 --res dd --tc 1.64572696728365737:1.59e-9 --commit 7671bd89 --allow_unraw > $O/lastnode.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
