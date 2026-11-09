#!/usr/bin/env bash
# #256: K 39, J 1000, 1280 bits at omega/omega_inf 1.09, 1.10, 1.11, the three nodes at once, --procs 3 each, beside #228 and #247.
# From solver/inner_amp/ of D:\choptuik-large-d, Python 3.14.10 (venv-t177), Normal priority, no affinity, no memory guard
# (mem_watch.sh only alerts). Exit codes go to exits.txt.
cd /d/choptuik-large-d/solver/inner_amp || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=/d/choptuik-large-d-raw/I256-win2
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
free() { powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"; }
echo "start $(stamp), free $(free) GB" >> $R/exits.txt
for wf in 1.09 1.10 1.11; do
  ( t=$(date +%s)
    "$PY" -u amp_flint_par.py $wf 39 1000 1280 --procs 3 --fit phys --mf 6:12 --out $R/sigF_w${wf}_K39_J1000_p1280.json > $R/w$wf.log 2>&1; rc=$?
    echo "w$wf exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt ) &
done
wait
echo "done $(stamp)" >> $R/exits.txt
