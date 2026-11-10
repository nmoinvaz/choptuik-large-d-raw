#!/bin/zsh
# planted truth (C6) and its mutations, run first; from solver/inner_pert/ of the worktree
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac      # raw-data clone at 07a860b6
PY=/Users/nathan/venv-314/bin/python
F=($R/fields/fields_D*.npz)
nice -n 10 $PY nnlo_closed_form.py planted $F --json=out/planted.json > out/planted.log 2>&1; echo "planted $?" > out/exits.txt
for m in k1x0 k2x-1 k2x1.1; do
  nice -n 10 $PY nnlo_closed_form.py planted $F --mutate=$m --json=out/planted_mut_$m.json > out/planted_mut_$m.log 2>&1
  echo "planted --mutate=$m $?" >> out/exits.txt
done
# remainder at the real NNLO's size (information, not a criterion: P3's K1 range is expected to fail)
nice -n 10 $PY nnlo_closed_form.py planted $F --plant_scale=740 --json=out/planted_big.json > out/planted_big.log 2>&1
echo "planted --plant_scale=740 $? (information)" >> out/exits.txt
