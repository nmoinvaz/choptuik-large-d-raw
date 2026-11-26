#!/bin/bash
# D 2000 release at L = 20, h13 with the quad-double Jacobian solved in quad-double (#1088; form_s.py release_ls at
# 6c1f2b7e or later, jac qq): from out/rls2000c's h11 state (h5-h11 released); there h13's inner solves with the qd
# Jacobian and a dd solve floored at 7.6e-34 to 1.9e-37 against the target residual 2.5e-37; the quad-double residual,
# each accepted outer step's state saved, the full system's record (system "full", released_from) with the octo-double
# check and the Hamiltonian check; held Delta (out/L2000) given for held -> full; Track C 1.649074313886 +- 1.2e-9;
# the corrected refit's prediction 1.64907431374585 +- 1.50e-11; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q 'solve="qd" if jk == "qq"' $W/hp/form_s.py || exit 1
S=$W/out/rls2000c/release_ls_h11_D2000.0000.npz
[ -s $S ] || exit 1
O=$W/out/rls2000d
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s.py release_ls $S $O --harm 13 --jac_by 13:qq --res qd \
  --threads 10 --outer 6 --held_delta 1.649074313361931285863151192710620626890 --tc 1.649074313886:1.2e-9 --commit 51a8e3be --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
