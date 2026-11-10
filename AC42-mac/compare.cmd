#!/bin/zsh
# the closed form against the stored solutions, its controls and mutations; from solver/inner_pert/ of the worktree
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac      # raw-data clone at 07a860b6
PY=/Users/nathan/venv-314/bin/python
F=($R/fields/fields_D*.npz)
nice -n 10 $PY nnlo_closed_form.py compare $F --figs=$R/figs.json --spread=$R/fields_t140_d6,$R/fields_t140_d10 \
  --json=out/compare.json --kout=out/closed_form_K.json > out/compare.log 2>&1; echo "compare $?" >> out/exits.txt
nice -n 10 $PY nnlo_closed_form.py controls $F --figs=$R/figs.json --json=out/controls.json > out/controls.log 2>&1
echo "controls $?" >> out/exits.txt
for m in k1x0 k2x-1; do
  nice -n 10 $PY nnlo_closed_form.py compare $F --figs=$R/figs.json --mutate=$m --json=out/compare_mut_$m.json \
    > out/compare_mut_$m.log 2>&1; echo "compare --mutate=$m $?" >> out/exits.txt
done
# resolution scan (information): which scale of K1 or K2 the test resolves; exit 1 means the scale is not resolved
for m in k2x0.5 k2x1.1 k2x1.5 k2x2 k1x0.99 k1x1.01 k1x1.02 k1x1.05; do
  nice -n 10 $PY nnlo_closed_form.py compare $F --figs=$R/figs.json --mutate=$m \
    > out/compare_mut_$m.log 2>&1; echo "compare --mutate=$m $? (resolution scan)" >> out/exits.txt
done
