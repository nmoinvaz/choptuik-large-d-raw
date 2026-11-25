#!/bin/bash
# the last node at the anti-Stokes point x_c = 1/sqrt 2 - 0.79/n (#1088; form_s_lastnode.py solve): T1 D 2200 (from the
# held states at D 1000, 1414, 2000, as the old layout's D 2200 jump), T3 D 2420 and T4 D 2828.4271 (each from the last
# three converged states); held, the Moebius horizon a 8 at x_c, ks 1.5 n + 20, kc 250, the double-double Jacobian and
# residual to Delta's bound 1e-15, the quad-double check, the Hamiltonian check; references: the old layout's D 2200
# held Delta, the #1095 refit at D 2420 and 2828.4271; stops at the first that does not converge; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
bash $W/update_py.sh > /dev/null
grep -q "the path runs outward only" $W/hp/form_s_lastnode.py || exit 1
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2
S1=$W/out/j1000_held_mob/jump_s_D1000.0000.npz
S2=$W/out/j1414_held_mob/jump_s_D1414.0000.npz
S3=$W/out/j2000_held_mob2/jump_s_D2000.0000.npz
for spec in 2200:1.648603934722933:1e-12 2420:1.64817621790898:5.3e-10 2828.4271247461903:1.64755842103839:5.7e-10; do
  D=${spec%%:*}; TC=${spec#*:}
  O=$W/out/xc$(echo $D | cut -c1-4)
  mkdir -p $O
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
  $PY -u form_s_lastnode.py solve $O --D $D --states_s "$S1,$S2,$S3" --xl xc --threads 10 --tc $TC --commit 63ff22ca \
    --allow_unraw > $O/lastnode.log 2>&1
  echo "rc $?" >> $O/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
  grep -q "  converged;" $O/lastnode.log || exit 1
  S1=$S2; S2=$S3; S3=$(ls $O/lastnode_D*.npz)
done
exit
}
