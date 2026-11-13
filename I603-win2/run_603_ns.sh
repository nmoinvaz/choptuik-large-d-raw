#!/usr/bin/env bash
# #603 second restart (the coordinator's standing instruction, message 1794578121158-0): chain_nat's command with --od_strong 4 added, from chain_nat's newest converged state, into chain_ns/ (log chain_ns.log).
# usage: S=I603-win2/chain_nat/anm_pin3_D<newest>.npz A0=<twice the last accepted a> bash run_603_ns.sh
# Worktree D:/choptuik-i603n at origin/main aedb403b or later (must have --od_strong, which main 58628d94 has; aedb403b descends from it), venv-i600, 9 threads. The stop rule stays: the third refusal in a row at one D.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I603-win2
: "${S:?S is the start state, relative to the raw clone}" "${A0:?A0 is twice the last accepted a}"
cd /d/choptuik-i603n/hp || exit 9
git merge-base --is-ancestor 58628d94 HEAD || { echo "worktree D:/choptuik-i603n has no --od_strong" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "603 chain_ns start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S a0 $A0" >> $R/exits_603.txt
"$PY" -u anm_run.py $RAW $R/chain_ns --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --a0 $A0 > $R/chain_ns.log 2>&1
rc=$?
echo "603 chain_ns anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_603.txt
