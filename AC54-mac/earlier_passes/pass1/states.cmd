# from solver/inner_pert/ of /Users/nathan/Source/choptuik-ac54 at 3e924b8; raw clone at d4d8258d
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
nice -n 10 /Users/nathan/venv-314/bin/python ainf_from_states.py states $R/fields/fields_D*.npz --chains=$R/fields_t140_d6,$R/fields_t140_d10 --json=$S/states.json --summary=$S/summary.json > $S/states.log 2>&1
