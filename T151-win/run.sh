#!/bin/bash
# T151 checks on the multidouble 4.0.0 build, outputs in T151-win, exit codes in exits.txt
export PATH=/c/Users/nathan/Source/venv-t151/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t151 RAYON_NUM_THREADS=4
R=/c/Users/nathan/Source/choptuik-large-d-raw; O=$R/T151-win
cd /c/Users/nathan/Source/choptuik-t151/hp
: > $O/exits.txt
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
J=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json
python highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 > $O/highm_ref.log 2>&1; echo "highm_ref exit $? $(t)" >> $O/exits.txt
python highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json > $O/highm_scaled.log 2>&1; echo "highm_scaled exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J > $O/highm_jets.log 2>&1; echo "highm_jets exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J --mutate=kappa > $O/highm_jets_mutate_kappa.log 2>&1; echo "highm_jets_mutate_kappa exit $? $(t)" >> $O/exits.txt
python ojet_check.py ../../choptuik-large-d-raw ../../choptuik-large-d-raw/T151-win/ojet_T113_D148.jsonl --state T113-win/chain/anm_pin3_D148.7434.npz --N 24 --threads 4 --check 0 > $O/ojet_check.log 2>&1; echo "ojet_check exit $? $(t)" >> $O/exits.txt
python full_release.py ../../choptuik-large-d-raw anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz --kfreeze 13 --octo 1 --junk 4 --it 1 --threads 4 > $O/release_D79.7657.log 2>&1; echo "full_release exit $? $(t)" >> $O/exits.txt
echo done >> $O/exits.txt
