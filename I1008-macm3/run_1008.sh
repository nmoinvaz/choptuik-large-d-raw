#!/bin/bash
# #1008 (the coordinator, 2026-11-19): the order-135 chain across its fold by arclength, from #903's last accepted base
# chain_k135b/anm_pin3_D259.1072.npz (D 259.107228285). Usage: run_1008.sh pilot|full STEPS CAP_SECONDS [STATE]
# The flags F are run_903_k135b.sh's F unchanged (--qd_it 40), plus --arclength 1 --arc_sign 1 --turns_max 2 (--save_jet 1 is in F) and
# #842's arc flags as its crossing run used them (I842-dh610/run842.sh: --arc_dhold 1e-12; --guard 0.05 and --border 1 are the defaults,
# given explicitly). --a0 0.0455 is the arclength step of the first attempt (#842 used 0.00097 near its fold at D 259.8875): half of the
# 0.0909 that #903's step 53 refused, the next a its D chain would have tried. Code: worktree choptuik-large-d-1008 at main d68818a4
# (hp/arclength.py), venv-macm3-main (hpkernel 1f3cda09 build: no Solver.series_o, no octo_tangents, taken with notices), 6 threads,
# nice 10 under caffeinate.
# pilot2 (2026-11-19): the same, on main 997072bd (arclength.py: a corrector iterate with D outside D > 2 raises ValueError, #1008), with
# EXTRA="--arc_jet <pilot/arcjet_000_D259.107228.npz>" so the series of the first pilot is read, not formed again. Output pilot2/, log pilot2.log.
MODE=$1; STEPS=$2; CAP=$3
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1008-macm3
PY=$HOME/Source/venv-macm3-main/bin/python
STATE=${4:-I903-macm3/chain_k135b/anm_pin3_D259.1072.npz}
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 40 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
ARC="--arclength 1 --arc_sign 1 --turns_max 2 --guard 0.05 --border 1 --arc_dhold 1e-12 --a0 0.0455"
ARC="$ARC $EXTRA"       # EXTRA: more flags, for pilot2 --arc_jet <abs path of pilot/arcjet_000_D259.107228.npz>
cd $HOME/Source/choptuik-large-d-1008/hp || exit 9
log() { echo "1008m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1008.txt; }
log "$MODE start, main $(git rev-parse --short=8 HEAD), state $STATE, steps $STEPS, cap $CAP s"
t=$(date +%s)
caffeinate -is nice -n 10 $PY -u $O/capped_run.py $CAP $PY -u anm_run.py $RAW $O/$MODE --state $STATE $F --ks 135 --keep_plan 1 --steps $STEPS --D_max 262 $ARC > $O/$MODE.log 2>&1
rc=$?
log "$MODE exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
