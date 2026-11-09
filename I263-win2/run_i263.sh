#!/usr/bin/env bash
# #263: main's count-independent amp_flint_par.py (64914d8, #246) at K 33, J 1000, 960 bits, omega/omega_inf 1.10, --procs 2 and 3 at once.
# From solver/inner_amp/ of the fresh worktree D:\choptuik-i263 (detached at f57c976, main), separate from the pinned checkout
# D:\choptuik-large-d (188853c, for #228 and #256). Python 3.14.10 (venv-t177), Normal priority, no affinity. Argument: the counts to
# run at once (default "2 3"; one at a time if memory is short).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=/d/choptuik-large-d-raw/I263-win2
cd /d/choptuik-i263/solver/inner_amp || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
free() { powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"; }
COUNTS=${1:-"2 3"}
echo "start counts [$COUNTS] $(stamp), free $(free) GB, worktree $(git -C /d/choptuik-i263 rev-parse --short HEAD)" >> $R/exits.txt
for n in $COUNTS; do
  ( t=$(date +%s)
    "$PY" -u amp_flint_par.py 1.10 33 1000 960 --procs $n --fit phys --mf 6:12 --out $R/sigF_w1.10_K33_J1000_main_procs${n}.json > $R/main_procs${n}.log 2>&1; rc=$?
    echo "main procs$n exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt ) &
done
wait
echo "done [$COUNTS] $(stamp)" >> $R/exits.txt
