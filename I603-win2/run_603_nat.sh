#!/usr/bin/env bash
# #603 restart (the coordinator, message 1794574919593-0, 2026-11-13 13:0x UTC): the chain from its newest converged state with the natural test, a higher iteration cap and the series kept.
# Start: I603-win2/chain/anm_pin3_D253.7313.npz (the old run, run_603.sh, was stopped between attempts at 13:03:25 UTC, 51 states). Output chain_nat/, log chain_nat.log.
# Changes from run_603.sh: --od_accept natural, --qd_it 20 (from 12), --save_jet 1 (each base's series, for #685), --a0 0.0556 (twice the last accepted a). Worktree D:/choptuik-i603n at origin/main aedb403b
# (--od_accept natural, --save_jet and the corrected summary residual), venv-i600 as before, 9 threads. The stop rule stays: the third refusal in a row at one D.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I603-win2
S=I603-win2/chain/anm_pin3_D253.7313.npz
cd /d/choptuik-i603n/hp || exit 9
git merge-base --is-ancestor aedb403b HEAD || { echo "worktree D:/choptuik-i603n is older than aedb403b" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "603 chain_nat start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits_603.txt
"$PY" -u anm_run.py $RAW $R/chain_nat --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --a0 0.0556 > $R/chain_nat.log 2>&1
rc=$?
echo "603 chain_nat anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_603.txt
