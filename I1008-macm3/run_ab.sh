#!/bin/bash
# #1008 AB runs (the coordinator's order, 2026-11-20): run_1008.sh's command with its flags F and ARC unchanged, except that --a0 is
# $A0 (run_1008.sh fixes it at 0.0455, and anm_run's parser takes an option once) and EXTRA adds --elim_switch 0 and --arc_jet.
# Usage: A0=<a> EXTRA="..." run_ab.sh MODE STEPS CAP_SECONDS STATE     (the same code worktree choptuik-large-d-1008, the same venv)
MODE=$1; STEPS=$2; CAP=$3; STATE=$4
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1008-macm3
PY=$HOME/Source/venv-macm3-main/bin/python
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 40 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
ARC="--arclength 1 --arc_sign 1 --turns_max 2 --guard 0.05 --border 1 --arc_dhold 1e-12 --a0 $A0"
ARC="$ARC $EXTRA"
cd $HOME/Source/choptuik-large-d-1008/hp || exit 9
log() { echo "1008m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1008.txt; }
log "$MODE start, main $(git rev-parse HEAD), state $STATE, steps $STEPS, cap $CAP s, a0 $A0, extra: $EXTRA"
t=$(date +%s)
caffeinate -is nice -n 10 $PY -u $O/capped_run.py $CAP $PY -u anm_run.py $RAW $O/$MODE --state $STATE $F --ks 135 --keep_plan 1 --steps $STEPS --D_max 262 $ARC > $O/$MODE.log 2>&1
rc=$?
log "$MODE exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
