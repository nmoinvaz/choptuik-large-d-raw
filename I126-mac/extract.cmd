#!/bin/zsh
# Fields of every state used (run from anywhere; writes I126-mac/fields/ and extract.log)
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aad2528b106a4fd00
R=/Users/nathan/Source/choptuik-large-d-raw
PY=/Users/nathan/Source/venv-anm/bin/python
S=$W/hp/data/states
DD=()
for f in $S/up*_D*.npz; do
  d=${f##*_D}; d=${d%.npz}; d=${d%%.*}
  if (( d >= 15 )); then DD+=($f); fi
done
QD=($R/T81/conv_pin5_D73.0000_D73.000000.npz)
for d in 80 90 100 110 120 130 140 150 160 170; do QD+=($R/T138-win2/chain/anm_pin3_D$d.0000.npz); done
for d in 180 190 200 205 209 215; do QD+=($R/T138-win2/chain_o/anm_pin3_D$d.0000.npz); done
nice -n 10 $PY $W/solver/inner_pert/nnlo_vs_solution.py extract $R/I126-mac/fields $DD $QD
# the spread between chains at equal D
nice -n 10 $PY $W/solver/inner_pert/nnlo_vs_solution.py extract $R/I126-mac/fields_t140_d6 $R/T140-win/chain_d6/anm_pin3_D100.0000.npz $R/T140-win/chain_d6/anm_pin3_D150.0000.npz $R/I13-win/chain_d6/anm_pin3_D180.0000.npz
nice -n 10 $PY $W/solver/inner_pert/nnlo_vs_solution.py extract $R/I126-mac/fields_t140_d10 $R/T140-win/chain_d10/anm_pin3_D100.0000.npz $R/T140-win/chain_d10/anm_pin3_D150.0000.npz $R/I13-win/chain_d10/anm_pin3_D180.0000.npz
