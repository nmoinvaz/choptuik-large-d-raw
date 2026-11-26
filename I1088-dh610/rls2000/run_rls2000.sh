#!/bin/bash
# D 2000 release at L = 20 (#1088; form_s.py release_ls at afcf9b0d): p1's harmonics 5, 7, 9, 11 released in turn (13 after the D 1000 test of the quad-double Jacobian)
# from the held solve of out/L2000 (the full system and its record come with h13); the quad-double residual (25.5 s against
# 255 s in octo-double at this ks on the Mac, I1088-mac-a/form_s/time_res/), the double-double Jacobian, the octo-double
# end check, the Hamiltonian check; each accepted outer step's state saved; Track C 1.649074313886 +- 1.2e-9; 4 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
grep -q 'chk = "od" if o\["res"\] == "qd"' $W/hp/form_s.py || exit 1
S=$W/out/L2000/lastnode_D2000.0000.npz
[ -s $S ] || exit 1
O=$W/out/rls2000
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s.py release_ls $S $O --harm 5,7,9,11 --res qd \
  --threads 4 --outer 6 --tc 1.649074313886:1.2e-9 --commit afcf9b0d --allow_unraw > $O/rls.log 2>&1
echo "rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
