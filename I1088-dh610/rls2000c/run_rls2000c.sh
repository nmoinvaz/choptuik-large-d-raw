#!/bin/bash
# D 2000 release at L = 20, h11 and h13 with the quad-double Jacobian (#1088; form_s.py release_ls at 1ccd32ab): from
# out/rls2000b's h9 state (h5-h9 released); there h11 with the double-double Jacobian stopped its inner solve at the
# floor 2.7e-28, above the target residual 4.8e-33 (as h13 did at D 1000); the quad-double residual, each accepted outer
# step's state saved, the full system's record with the octo-double check and the Hamiltonian check; held Delta
# (out/L2000) given for held -> full; Track C 1.649074313886 +- 1.2e-9; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q 'jac_by = {int(a)' $W/hp/form_s.py || exit 1
S=$W/out/rls2000b/release_ls_h9_D2000.0000.npz
[ -s $S ] || exit 1
O=$W/out/rls2000c
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s.py release_ls $S $O --harm 11,13 --jac_by 11:qd,13:qd --res qd \
  --threads 10 --outer 6 --held_delta 1.649074313361931285863151192710620626890 --tc 1.649074313886:1.2e-9 --commit 1ccd32ab --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
