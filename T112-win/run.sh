#!/bin/bash
# T112 checks, each command's output in T112-win, exit codes in exits.txt
export PATH=/c/Users/nathan/Source/venv-t112/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t112 RAYON_NUM_THREADS=4
R=/c/Users/nathan/Source/choptuik-large-d-raw; O=$R/T112-win
cd /c/Users/nathan/Source/choptuik-t112/hp
: > $O/exits.txt
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
J=../../choptuik-large-d-raw/anm-mac/release210/jets_200.json
python highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 > $O/highm_ref.log 2>&1; echo "highm_ref exit $? $(t)" >> $O/exits.txt
python highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json > $O/highm_scaled.log 2>&1; echo "highm_scaled exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J > $O/highm_jets.log 2>&1; echo "highm_jets exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J --mutate=kappa > $O/highm_jets_mutate_kappa.log 2>&1; echo "highm_jets_mutate_kappa exit $? $(t)" >> $O/exits.txt
echo done >> $O/exits.txt
