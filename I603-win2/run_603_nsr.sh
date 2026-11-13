#!/usr/bin/env bash
# #603 third restart (the coordinator, message 1794589331279-0, 2026-11-13 17:0x UTC): chain_ns's command with --reseed_start pred added (the re-seed's quad-double polish starts from the prediction's own four-part horizon data,
# about 1e-39 off, instead of the double-double ladder's, about 1e-32 off: #693), from chain_ns's newest converged state, into chain_nsr/ (log chain_nsr.log). --od_accept natural and --od_strong 4 stay.
# usage: S=I603-win2/chain_ns/anm_pin3_D<newest>.npz A0=<twice the last accepted a> bash run_603_nsr.sh
# Worktree D:/choptuik-i603r at origin/main a515ab87 or later, venv-i600, 9 threads. The stop rule stays: the third refusal in a row at one D.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I603-win2
: "${S:?S is the start state, relative to the raw clone}" "${A0:?A0 is twice the last accepted a}"
cd /d/choptuik-i603r/hp || exit 9
git merge-base --is-ancestor a515ab87 HEAD || { echo "worktree D:/choptuik-i603r is older than a515ab87" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "603 chain_nsr start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S a0 $A0" >> $R/exits_603.txt
"$PY" -u anm_run.py $RAW $R/chain_nsr --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a0 $A0 > $R/chain_nsr.log 2>&1
rc=$?
echo "603 chain_nsr anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_603.txt
