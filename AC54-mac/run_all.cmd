#!/bin/zsh
# every run of agent-comms#54, in order; from solver/inner_pert/ of /Users/nathan/Source/choptuik-ac54 (the commit is
# printed first in exits.txt); the raw-data clone at d4d8258d. One process at a time, nice -n 10.
S=/Users/nathan/Source/choptuik-large-d-raw-staging/AC54-mac
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
PY=/Users/nathan/venv-314/bin/python
F=($R/fields/fields_D*.npz)
SUM=data/ainf_from_states.json
cd /Users/nathan/Source/choptuik-ac54/solver/inner_pert
echo "code $(git rev-parse --short HEAD), $(date -u '+%Y-%m-%d %H:%M') UTC" >> $S/exits.txt
run() { local name=$1; shift; nice -n 10 $PY ainf_from_states.py "$@" > $S/$name.log 2>&1; echo "$name -> exit $?" >> $S/exits.txt; }
run selection selection --json=$S/selection.json
run planted planted $F --json=$S/planted.json --summary=$SUM
run planted_mut_offset planted $F --family=alt12,cpx7 --mutate=offset --json=$S/planted_mut_offset.json --summary=$SUM
run states states $F --chains=$R/fields_t140_d6,$R/fields_t140_d10 --json=$S/states.json --summary=$SUM
run controls controls $F --json=$S/controls.json --summary=$SUM
for m in shift slope step; do run states_mut_$m states $F --mutate=$m --json=$S/states_mut_$m.json; done
# P3, after the real run: the reference fit's rms residual in A_n (states.log, 8.85e-10) as planted noise, 20 seeds
run planted_noise planted $F --family=alt12,cpx7 --noise=8.85e-10 --seeds=20 --json=$S/planted_noise.json --summary=$SUM
