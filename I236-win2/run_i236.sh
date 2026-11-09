#!/usr/bin/env bash
# #236: K 25 J 1000 at 1.10 with --procs 1..4, runs r1 then r2, the four counts of a run at once. Normal priority, no affinity.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=/d/choptuik-large-d-raw/I236-win2
cd /d/choptuik-large-d/solver/inner_amp || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
free() { powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"; }
for r in r1 r2; do
  echo "batch $r start $(stamp), free $(free) GB" >> $R/exits.txt
  for n in 1 2 3 4; do
    ( t=$(date +%s)
      "$PY" -u amp_flint_par.py 1.10 25 1000 960 --procs $n --fit phys --mf 6:12 --out $R/sigF_w1.10_K25_J1000_procs${n}_$r.json > $R/procs${n}_$r.log 2>&1; rc=$?
      echo "procs$n $r exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt ) &
  done
  wait
  echo "batch $r end $(stamp)" >> $R/exits.txt
done
echo "all done $(stamp)" >> $R/exits.txt
