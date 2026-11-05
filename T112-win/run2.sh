#!/bin/bash
# T112 jets check against the stored-plan reference (cloud 2026-11-05 18:55 UTC), 2 threads
export PATH=/c/Users/nathan/Source/venv-t112/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t112 RAYON_NUM_THREADS=2
R=/c/Users/nathan/Source/choptuik-large-d-raw; O=$R/T112-win
cd /c/Users/nathan/Source/choptuik-t112/hp
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
J=../../choptuik-large-d-raw/anm-mac/jets_plans/jets_plans.json
python highm_check.py jets --compare=$J > $O/jets_plans.log 2>&1; echo "jets_plans exit $? $(t)" >> $O/exits.txt
python highm_check.py jets --compare=$J --mutate=kappa > $O/jets_plans_kappa.log 2>&1; echo "jets_plans_kappa exit $? $(t)" >> $O/exits.txt
echo done2 >> $O/exits.txt
