#!/usr/bin/env bash
# #489: the base polish of a re-noded state at its D with crawlJ's options (I461-win2/run_i461_j.sh), --steps 0 and
# --save_base 1, 2 threads under nice 10. Usage: run_polish.sh WORKTREE_HP RAW STATE TAG (STATE relative to RAW).
HP=$1
RAW=$2
S=$3
TAG=$4
R=$RAW/I489-mac
PY=/Users/nathan/venv-314/bin/python
cd "$HP" || exit 9
echo "polish $TAG start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S at $(git rev-parse --short=7 HEAD)" >> "$R/exits.txt"
t=$(date +%s)
nice -n 10 "$PY" -u anm_run.py "$RAW" "$R/$TAG" --state "$S" --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 0 --D_max 400 --threads 2 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 \
   --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 > "$R/$TAG.log" 2>&1
rc=$?
echo "polish $TAG exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$R/exits.txt"
