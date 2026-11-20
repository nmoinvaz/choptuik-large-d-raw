#!/bin/bash
# #1008 restart (the coordinator's order, 2026-11-20 about 20:15 UTC): run_ab.sh's command with its flags F and ARC unchanged, started from run2's last
# accepted arc state on venv-macm3-1058b (hp at main 8179068d) instead of venv-macm3-main, and (the coordinator's answer, 2026-11-20 about 20:40 UTC) the code
# from a new worktree choptuik-large-d-1008b at 8179068d, so that code and kernel come from one commit (run2 ran the code of choptuik-large-d-1008 at 9980cd93).
# Usage: run_restart.sh MODE STEPS CAP_SECONDS STATE A0 [ARC_JET]     (EXTRA is run_ab.sh's "--elim_switch 0"; ARC_JET adds --arc_jet FILE)
MODE=$1; STEPS=$2; CAP=$3; STATE=$4; A0=$5; JET=$6
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1008-macm3
PY=${R1008_PY:-$HOME/Source/venv-macm3-1058b/bin/python}
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 40 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
ARC="--arclength 1 --arc_sign 1 --turns_max 2 --guard 0.05 --border 1 --arc_dhold 1e-12 --a0 $A0"
EXTRA="--elim_switch 0"
[ -n "$JET" ] && EXTRA="$EXTRA --arc_jet $JET"
ARC="$ARC $EXTRA"
cd ${R1008_CODE:-$HOME/Source/choptuik-large-d-1008b}/hp || exit 9
log() { echo "1008m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1008.txt; }
HK=$($PY -c "import hpkernel, multidouble, sys; print('hpkernel.__file__', hpkernel.__file__, 'isa', hpkernel.isa(), 'multidouble isa', multidouble.isa(), 'multidouble', multidouble.__file__, 'python', sys.version.split()[0])" 2>&1 | tr '\n' ' ')
log "$MODE start, code main $(git rev-parse HEAD), venv $PY: $HK; state $STATE, steps $STEPS, cap $CAP s, a0 $A0, extra: $EXTRA"
t=$(date +%s)
caffeinate -is nice -n 10 $PY -u $O/capped_run.py $CAP $PY -u anm_run.py $RAW $O/$MODE --state $STATE $F --ks 135 --keep_plan 1 --steps $STEPS --D_max 262 $ARC > $O/$MODE.log 2>&1
rc=$?
log "$MODE exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
