#!/bin/bash
# D 5656.8542 held at L = 20 (#1088; form_s_lastnode.py solvestate at f5eb570f): the guess of out/g5657L20 (built on the
# Mac, I1088-mac-a/form_s/g5657L20/), on the precision ladder: 2 steps with the double-double residual (out/L5657
# reached 1.2e-20 in 2 and its floor, 4.3e-21, in 3), then up to 2 with the quad-double residual, each with the
# double-double Jacobian, to Delta's bound 1e-15; each step's state saved; the octo-double check, the Hamiltonian
# check; Track C's 1.64572696728365737 +- 1.59e-9 for the comparison; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "def newton_ladder" $W/hp/form_s.py || exit 1
O=$W/out/L5657q
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py solvestate $O --state $W/out/g5657L20/guess_D5656.8542.npz \
  --threads 6 --ladder dd,qd --it_max 2 --it_hi 2 --delta_tol 1e-15 --tc 1.64572696728365737:1.59e-9 --commit f5eb570f --allow_unraw > $O/lastnode.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
