#!/usr/bin/env bash
# #236 mechanism test: the same K 25 J 1000 case at 1.10 with amp_flint_par_fixsum.py (fixed summation order), --procs 1..4, one
# run each, the four at once, after run_i236.sh has finished. Normal priority, no affinity.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
R=/d/choptuik-large-d-raw/I236-win2
cd /d/choptuik-large-d/solver/inner_amp || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
echo "fixsum batch start $(stamp)" >> $R/exits_fixsum.txt
for n in 1 2 3 4; do
  ( t=$(date +%s)
    "$PY" -u $R/amp_flint_par_fixsum.py 1.10 25 1000 960 --procs $n --fit phys --mf 6:12 --out $R/sigF_w1.10_K25_J1000_fixsum_procs${n}_r1.json > $R/fixsum_procs${n}_r1.log 2>&1; rc=$?
    echo "fixsum procs$n r1 exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits_fixsum.txt ) &
done
wait
echo "fixsum all done $(stamp)" >> $R/exits_fixsum.txt
