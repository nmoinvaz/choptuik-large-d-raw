#!/usr/bin/env bash
# #140 control, rp = 0.081 in place of the issue's 0.079, which lemma6_jump_M.py refuses (ValueError: Z beyond the real
# reach of D; Z = 0.004489 is fixed and rp = 0.08 just reaches it). The coordinator approved 0.081 on 2026-11-08.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
R=C:/Users/nathan/Source/choptuik-large-d-raw
D=$R/I140-win2
EX=$D/exits.txt
cd /c/Users/nathan/Source/choptuik-i140/solver/proof || exit 9
t=$(date +%s)
"$PY" -u lemma6_jump_M.py --M=5 --box=$R/I104-win2/A_M2_6a_M5_sub1e-18.json --rp=0.081 --k=20 \
  --save-B=$D/B_control.json --json=$D/l6a_control.json > $D/l6a_control.log 2>&1
rc=$?
echo "l6a_control_rp0.081 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX
