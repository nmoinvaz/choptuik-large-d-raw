#!/usr/bin/env bash
# #247: the fixed-order sum (amp_flint_par_fixsum.py of I236-win2) at K 33, J 1000, 1.10, --procs 2 and 3. Argument: the counts to run
# at once (default "2 3"; one at a time as "2" then "3" if memory is short). Normal priority, no affinity.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I247-win2
cd /d/choptuik-large-d/solver/inner_amp || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
free() { powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"; }
COUNTS=${1:-"2 3"}
echo "start counts [$COUNTS] $(stamp), free $(free) GB" >> $R/exits.txt
for n in $COUNTS; do
  ( t=$(date +%s)
    "$PY" -u $RAW/I236-win2/amp_flint_par_fixsum.py 1.10 33 1000 960 --procs $n --fit phys --mf 6:12 --out $R/sigF_w1.10_K33_J1000_fixsum_procs${n}.json > $R/fixsum_procs${n}.log 2>&1; rc=$?
    echo "fixsum procs$n exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt ) &
done
wait
echo "done [$COUNTS] $(stamp)" >> $R/exits.txt
