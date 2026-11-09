#!/usr/bin/env bash
# #229: the K 33 J 1000 node at 1.10 with --procs 2 (macm3's count), as I202-win2's run otherwise. Normal priority, no affinity.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=/d/choptuik-large-d-raw/I229-win2
cd /d/choptuik-large-d/solver/inner_amp || exit 9
t=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u amp_flint_par.py 1.10 33 1000 960 --procs 2 --fit phys --mf 6:12 --out $R/sigF_w1.10_K33_J1000_procs2.json > $R/w1.10_procs2.log 2>&1
rc=$?
echo "amp_flint_par K33 J1000 w1.10 procs2 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
