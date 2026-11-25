#!/bin/bash
# after the second z-recurrence check (unit i1088a-zcheck2, build 815287c6): release p1's harmonics 5-13 at D 1000
# from the lean held state (release_ls: the double-double Jacobian, the octo-double residual), the full system's record
# with the held -> full change of Delta; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-zcheck2; do sleep 30; done
bash $W/update_py.sh > /dev/null
grep -q "held -> full dDelta" $W/hp/form_s.py || exit 1
cd $W/hp || exit 1
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s.py release_ls $W/out/j1000_lean/jump_s_D1000.0000.npz \
  $W/out/rls1000 --harm 5,7,9,11,13 --threads 6 --outer 6 --tc 1.654240854245:7.8e-10 --commit 5dede503 --allow_unraw \
  > $W/out/rls1000.log 2>&1
exit
}
