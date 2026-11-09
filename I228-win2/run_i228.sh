#!/usr/bin/env bash
# #228: #82's 1.10 node (K 45, J 1500, 1280 bits, --procs 3) on the new firmware, with #82's interpreter (venv-t126, Python 3.12.8).
# Normal priority, no affinity, no memory guard. From solver/inner_amp/ of D:\choptuik-large-d.
cd /d/choptuik-large-d/solver/inner_amp || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
R=/d/choptuik-large-d-raw/I228-win2
t=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u amp_flint_par.py 1.10 45 1500 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out $R/sigF_w1.10_K45_J1500_p1280.json > $R/w1.10.log 2>&1
rc=$?
echo "amp_flint_par K45 J1500 w1.10 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
