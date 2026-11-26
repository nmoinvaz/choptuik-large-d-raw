#!/bin/bash
# D 1000 release of harmonic 13 with the quad-double Jacobian (#1088; form_s.py release_ls at afcf9b0d): from dh370's h5-h11 release
# (I1088-dh370/rls1000/release_ls_h11_D1000.0000.npz, copied to out/rls1000_src/), to the full system and its
# direct_s record (quad-double check, Hamiltonian check); octo-double residual, double-double Jacobian, each accepted
# outer step's state saved; the dd-Jacobian run (rls1000h13) stopped at an inner floor of 6.6e-33 above the target's 9.7e-36; Track C 1.654240854245 +- 7.8e-10 for the comparison; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q "inner_floor" $W/hp/form_s.py || exit 1
O=$W/out/rls1000h13q
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s.py release_ls $W/out/rls1000_src/release_ls_h11_D1000.0000.npz \
  $O --harm 13 --jac qd --threads 6 --outer 6 --tc 1.654240854245:7.8e-10 --commit afcf9b0d --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
