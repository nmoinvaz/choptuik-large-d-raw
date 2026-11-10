# from solver/inner_pert/ of /Users/nathan/Source/choptuik-ac54 at 3e924b8; raw clone at d4d8258d
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py planted $R/fields/fields_D*.npz --json=$S/planted.json > $S/planted.log 2>&1
nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py planted $R/fields/fields_D*.npz --family=alt12,cpx7 --mutate=offset --json=$S/planted_mut_offset.json > $S/planted_mut_offset.log 2>&1
