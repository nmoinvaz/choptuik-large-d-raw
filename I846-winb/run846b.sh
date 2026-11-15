#!/bin/bash
# stage 2 of #846 (runner's launcher; the issue's five refine arms, one at a time, stops on a nonzero exit)
W=/c/Users/nathan/Source/choptuik-i846
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
O=$RAW/I846-winb
PY=/c/Users/nathan/Source/venv-t179/Scripts/python.exe
export OPENBLAS_NUM_THREADS=4
cd "$W/solver/matter" || exit 99
ts() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
arm() {  # tag seed D kc reg
  t=$1; seed=$2; D=$3; kc=$4; reg=$5
  echo "$t start $(ts)  (seed $seed, D $D, kc $kc, reg $reg)" >> "$O/exits_846.txt"
  $PY sigdss_run.py refine "$O/$seed" --D $D --eps 1 --kc_seed $kc --kc $kc --reg $reg --tag $t > "$O/log_$t.txt" 2>&1
  rc=$?
  cp data/sigdss_refine_$t.jsonl data/sigdss_sol_ref_${t}_*.npy "$O/" 2>> "$O/exits_846.txt"
  echo "$t exit $rc $(ts)" >> "$O/exits_846.txt"
  [ $rc -eq 0 ] || { echo "stopped at $t (exit $rc) $(ts)" >> "$O/exits_846.txt"; exit $rc; }
}
arm i846a seed_D9_kc15.npy  9  15 0
arm i846b seed_D9_kc23.npy  9  23 0
arm i846c seed_D10_kc15.npy 10 15 0
arm i846d seed_D10_kc15.npy 10 15 1e-8
arm i846e seed_D10_kc23.npy 10 23 0
echo "stage2 all done $(ts)" >> "$O/exits_846.txt"
