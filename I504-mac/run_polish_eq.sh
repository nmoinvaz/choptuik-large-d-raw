#!/usr/bin/env bash
# #504: #489's base polish (I489-mac/run_polish.sh, crawlJ's options, --steps 0 --save_base 1) through eq_test.py
# polish: newton_od with D_c from |J| at the corrector's start (near_null_eq's result scaling), every trial printed,
# D_c compared with #502's at the same state. 2 threads under nice 10.
# Usage: run_polish_eq.sh WORKTREE_HP RAW STATE TAG (STATE relative to RAW).
HP=$1
RAW=$2
S=$3
TAG=$4
R=$RAW/I504-mac
PY=/Users/nathan/venv-314/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
cd "$HP" || exit 9
echo "polish $TAG start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S at $(git rev-parse --short=7 HEAD)" >> "$R/exits.txt"
t=$(date +%s)
nice -n 10 "$PY" -u eq_test.py polish --Dc_ref "$RAW/I502-mac/L08_plant7.json" --Dc_out "$R/${TAG}_Dc.npy" --hist_out "$R/${TAG}_hist" \
   "$RAW" "$R/$TAG" --state "$S" --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 0 --D_max 400 --threads 2 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 \
   --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 > "$R/$TAG.log" 2>&1
rc=$?
echo "polish $TAG exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
exit $rc
