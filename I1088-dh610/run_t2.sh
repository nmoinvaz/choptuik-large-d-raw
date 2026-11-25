#!/bin/bash
# T2 (#1088): at D 2828.4271, the held guess's horizon block over its largest other block with the last node at 0.700
# (the control: the old failure), 0.703, 0.705, 0.70677 and 0.709; the guess from the held states at D 1000, 1414 and
# 2000 at degree 2, the Moebius horizon a 8 summed at the last node, ks 1.5 n + 20, kc 250; residuals only; 10 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
bash $W/update_py.sh > /dev/null
test -s $W/hp/form_s_lastnode.py || exit 1
cd $W/hp || exit 1
mkdir -p $W/out/t2
S="$W/out/j1000_held_mob/jump_s_D1000.0000.npz,$W/out/j1414_held_mob/jump_s_D1414.0000.npz,$W/out/j2000_held_mob2/jump_s_D2000.0000.npz"
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $(cat $W/python_path) -u form_s_lastnode.py ratio $W/out/t2 --D 2828.4271247461903 \
  --states_s "$S" --xl 0.700,0.703,0.705,0.70677,0.709 --threads 10 --allow_unraw > $W/out/t2/t2.log 2>&1
exit
}
