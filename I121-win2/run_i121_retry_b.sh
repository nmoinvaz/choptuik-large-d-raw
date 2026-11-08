#!/usr/bin/env bash
# #121 recovery: rows_b (--only=1,12,16) died in row 1 at disc 20/34 with exit 132 and no traceback. The same rows
# command, narrowed to one row per process, with PYTHONFAULTHANDLER=1 so a native crash prints its stack.
cd /c/Users/nathan/Source/choptuik-i121/solver/proof || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
R=C:/Users/nathan/Source/choptuik-large-d-raw/I121-win2
EX=$R/exits.txt
X=2.71857918921174241298383648012843280883,0.99922840320656778341382852244561290493,0.14920357491144750568385993252030607895,0.01471905249025135288037099322184756733,0.00840534690576166107173716067740959800,0.00147034518159157802673581431742815600
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
declare -A PID T0
for j in 1 12 16; do
  T0[$j]=$(date +%s)
  "$PY" -u lemma6b1_cover_M.py rows --M=5 --x=$X --h=1e-18 --tag=_cert --only=$j > $R/rows_retry_row$j.log 2>&1 &
  PID[$j]=$!
done
for j in 1 12 16; do
  wait ${PID[$j]}; rc=$?
  echo "retry_row$j exit $rc wall $(( $(date +%s) - ${T0[$j]} ))s $(stamp)" >> $EX
done
