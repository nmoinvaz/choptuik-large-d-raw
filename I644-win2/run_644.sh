#!/usr/bin/env bash
# #644: the A/B of the octo-double corrector's trial test on #603's refused step (D 248.6298 to 249.39, a 0.763). The coordinator's command (message 1794553286702-0), two runs one after the other, 9 threads each,
# BelowNormal (nice -n 5), OPENBLAS_NUM_THREADS=1, `own` (the control) first. Worktree D:/choptuik-i644 at origin/main 5b9059ec, venv-i600 (the #600 build, the kernel #603 runs on). #603's state and files are read in place.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I644-win2
cd /d/choptuik-i644/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "5b9059ec" ] || { echo "worktree D:/choptuik-i644 is not at 5b9059ec" >&2; exit 9; }
[ -f $RAW/I603-win2/chain/anm_pin3_D248.6298.npz ] || { echo "missing the D 248.6298 state" >&2; exit 9; }
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
for acc in own natural; do
  echo "$acc start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_644.txt
  nice -n 5 "$PY" -u anm_run.py $RAW $R/$acc --state I603-win2/chain/anm_pin3_D248.6298.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 9 \
     --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
     --a0 0.762939453125 --od_accept $acc > $R/$acc.log 2>&1
  echo "$acc exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_644.txt
done
