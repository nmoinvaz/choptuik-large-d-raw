#!/bin/bash
# the held states at D 1000, 1414 and 2000 on the nodes 0.3 ... 0.7, 0.8, 0.9 (form_s.py relayout, ks 200, re-solved at
# the same D), then the D 2828 jump from them on those nodes (degree 2 in 1/n, the Moebius horizon a 8 summed at 0.9,
# ks 200, kc 250, the lean defaults); 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
bash $W/update_py.sh > /dev/null
grep -q "def cmd_relayout" $W/hp/form_s.py || exit 1
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2
for st in j1000_held_mob/jump_s_D1000.0000.npz j1414_held_mob/jump_s_D1414.0000.npz j2000_held_mob2/jump_s_D2000.0000.npz; do
  D=$(basename $st | sed 's/jump_s_D\(.*\)\.0000\.npz/\1/')
  $PY -u form_s.py relayout $W/out/$st $W/out/rl$D --add 0.8,0.9 --ks 200 --solve 1 --threads 9 --commit 3aecf887 \
    --allow_unraw > $W/out/rl$D.log 2>&1
  grep -q "re-solved on the new nodes: converged" $W/out/rl$D.log || exit 1
done
S="$W/out/rl1000/relayout_solved_D1000.0000.npz,$W/out/rl1414/relayout_solved_D1414.0000.npz,$W/out/rl2000/relayout_solved_D2000.0000.npz"
export HP_COMMIT=3aecf887
$W/run_jump.sh 2828 225 2 0 0 9 rl --held 1 --it_max 12 --kc 250 --delta fit --mob 8 --states_s "$S" --ks 200 --tol 1e-300
exit
}
