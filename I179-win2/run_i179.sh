#!/bin/bash
# I179-win2 checks on the Python 3.14.10 build (venv-t177, hpkernel avx2 + multidouble f092018), outputs in I179-win2, exit
# codes in exits.txt. The commands of I179-win/run_i179.sh with --threads=1; the five checks run at once (each reads its
# inputs and writes only its own log), Normal priority, no affinity.
export PATH=/c/Users/nathan/Source/venv-t177/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t177 RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
RAW=/d/choptuik-large-d-raw; O=$RAW/I179-win2
cd /d/choptuik-large-d
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
echo "checks start $(t)" >> $O/exits.txt
J=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json
( python check_numbers.py --selftest > $O/check_numbers_selftest.log 2>&1; echo "check_numbers_selftest exit $? $(t)" >> $O/exits.txt ) &
cd hp
( python highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 --threads=1 > $O/highm_ref.log 2>&1; echo "highm_ref exit $? $(t)" >> $O/exits.txt ) &
( python highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json --threads=1 > $O/highm_scaled.log 2>&1; echo "highm_scaled exit $? $(t)" >> $O/exits.txt ) &
( python highm_check.py jets --compare=$J --threads=1 > $O/highm_jets.log 2>&1; echo "highm_jets exit $? $(t)" >> $O/exits.txt ) &
( python highm_check.py jets --compare=$J --mutate=kappa --threads=1 > $O/highm_jets_mutate_kappa.log 2>&1; echo "highm_jets_mutate_kappa exit $? $(t)" >> $O/exits.txt ) &
wait
echo "checks done $(t)" >> $O/exits.txt
