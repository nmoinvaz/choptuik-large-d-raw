#!/bin/bash
# I179 checks on the Python 3.14.10 build (venv-t179, hpkernel avx512 + multidouble 4.0.0), outputs in I179-win, exit
# codes in exits.txt. Same commands as T151-win/run.sh, but one thread, run at idle priority beside #13's chains.
export PATH=/c/Users/nathan/Source/venv-t179/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t179 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
RAW=/c/Users/nathan/Source/choptuik-large-d-raw; O=$RAW/I179-win
cd /c/Users/nathan/Source/choptuik-i179
: > $O/exits.txt
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
echo "start $(t)" >> $O/exits.txt
python check_numbers.py --selftest > $O/check_numbers_selftest.log 2>&1; echo "check_numbers_selftest exit $? $(t)" >> $O/exits.txt
cd hp
J=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json
python highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 --threads=1 > $O/highm_ref.log 2>&1; echo "highm_ref exit $? $(t)" >> $O/exits.txt
python highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json --threads=1 > $O/highm_scaled.log 2>&1; echo "highm_scaled exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J --threads=1 > $O/highm_jets.log 2>&1; echo "highm_jets exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J --mutate=kappa --threads=1 > $O/highm_jets_mutate_kappa.log 2>&1; echo "highm_jets_mutate_kappa exit $? $(t)" >> $O/exits.txt
echo done >> $O/exits.txt
