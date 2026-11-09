#!/usr/bin/env bash
# I213-win2: sigma at K 45, J 1250, 1280 bits at omega/omega_inf 1.09, 1.10, 1.11, the three nodes at once as #82 ran them
# (J 1500), each --procs 3. From solver/inner_amp/ of D:\choptuik-large-d, Python 3.14.10 (venv-t177), Normal priority,
# no memory guard. Exit codes go to exits.txt.
cd /d/choptuik-large-d/solver/inner_amp || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=../../../choptuik-large-d-raw/I213-win2
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
for wf in 1.09 1.10 1.11; do
  ( t=$(date +%s)
    "$PY" -u amp_flint_par.py $wf 45 1250 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out $R/sigF_w${wf}_K45_J1250_p1280.json > $R/w$wf.log 2>&1; rc=$?
    echo "w$wf exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt ) &
done
wait
echo "done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
