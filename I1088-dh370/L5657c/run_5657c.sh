#!/bin/bash
# D 5656.8542 held at L = 20 (#1088; form_s_lastnode.py solvestate at 7bf304b1), continued from L5657q's state after its
# first dd step (out/L5657q_step0.npz): one more dd step, then up to 2 chord steps with that step's Jacobian and the
# quad-double residual (a fresh Jacobian only when a chord step cuts max |F| by less than 10x) to Delta's bound 1e-15;
# each step's state and each Jacobian saved; the octo-double check, the discretization tails, the Hamiltonian check;
# Track C's 1.64572696728365737 +- 1.59e-9 for the comparison; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "def make_step" $W/hp/floor_stop_check.py || exit 1
O=$W/out/L5657c
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py solvestate $O --state $W/out/L5657q_step0.npz \
  --threads 6 --ladder dd,qd --it_max 1 --it_hi 2 --chord 1 --step_est 3622,900 --delta_tol 1e-15 --tc 1.64572696728365737:1.59e-9 --commit 7bf304b1 --allow_unraw > $O/lastnode.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
