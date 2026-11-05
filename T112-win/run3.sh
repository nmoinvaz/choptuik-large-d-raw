#!/bin/bash
# T112 jets check against the stored-input reference (cloud 2026-11-05 19:59 UTC), 2 threads
export PATH=/c/Users/nathan/Source/venv-t112/Scripts:$PATH
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-t112 RAYON_NUM_THREADS=2
R=/c/Users/nathan/Source/choptuik-large-d-raw; O=$R/T112-win
cd /c/Users/nathan/Source/choptuik-t112/hp
t() { /usr/bin/date -u '+%F %H:%M:%S'; }
python highm_check.py jets --compare=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json > $O/jets_inputs.log 2>&1; echo "jets_inputs exit $? $(t)" >> $O/exits.txt
echo done3 >> $O/exits.txt
