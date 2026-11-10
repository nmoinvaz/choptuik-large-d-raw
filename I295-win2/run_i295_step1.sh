#!/usr/bin/env bash
# #295 step 1: K 15, J 1500 at omega/omega_inf 1.10 with 3 processes, to test whether sigma_1..sigma_6 depend on K at J 1500.
# From solver/inner_amp/ of D:\choptuik-large-d at 188853c with venv-t126 (the checkout and interpreter of #82's and #228's files),
# Normal priority, no affinity. Waits for #287 to end (18 + 3 threads exceed this machine's 20).
R=/d/choptuik-large-d-raw/I295-win2
until grep -q 'exit' /d/choptuik-large-d-raw/I287-win2/exits.txt; do sleep 15; done
cd /d/choptuik-large-d/solver/inner_amp || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
t=$(date +%s)
echo "step 1 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u amp_flint_par.py 1.10 15 1500 1280 --procs 3 --fit phys --mf 6:12 --out $R/sigF_w1.10_K15_J1500_p1280.json > $R/w1.10_K15.log 2>&1
rc=$?
echo "step 1 amp_flint_par K15 J1500 w1.10 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
