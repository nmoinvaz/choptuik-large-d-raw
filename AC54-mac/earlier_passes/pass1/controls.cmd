# from solver/inner_pert/ of /Users/nathan/Source/choptuik-ac54 at 3e924b8; raw clone at d4d8258d
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py controls $R/fields/fields_D*.npz --json=$S/controls.json > $S/controls.log 2>&1
for m in shift slope step; do
  nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py states $R/fields/fields_D*.npz --mutate=$m --json=$S/states_mut_$m.json > $S/states_mut_$m.log 2>&1
done
# P3: the real reference fit's rms residual (states.log, 8.85e-10) as planted noise, 20 seeds
nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py planted $R/fields/fields_D*.npz --family=alt12,cpx7 --noise=8.85e-10 --seeds=20 --json=$S/planted_noise.json > $S/planted_noise.log 2>&1
