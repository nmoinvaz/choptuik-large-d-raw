#!/bin/bash
# #944 on dh170: one anm_run step from a stored chain state with --od_junk J, the chain's flags (run903.sh of I903-dh170,
# run903c.sh of I903-dh610), the 4.8.2 venv and main's code (the 935 worktree). usage: run944.sh NAME STATE KS JUNK [LIMIT_S] [EXTRA anm_run flags, one quoted word]
# STATE is relative to ~/scratch944 (copies of the committed raw files). Output: I944-dh170/NAME/, log NAME.log.
NAME=${1:?name} STATE=${2:?state} KS=${3:?ks} JUNK=${4:?junk} LIMIT=${5:-10800} EXTRA=${6:-}
WT=$HOME/Source/choptuik-large-d-935
PY=$WT/.venv/bin/python
SCR=$HOME/scratch944
OUT=$HOME/Source/choptuik-large-d-raw/I944-dh170
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 262 --threads 10 --corrector od
 --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk $JUNK --jet_o 1 --reseed 2 --reseed_q 1
 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
log() { echo "944 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_944.txt; }
[ -s $SCR/$STATE ] || { log "$NAME: missing $STATE"; exit 9; }
cd $WT/hp || exit 9
export PYTHONFAULTHANDLER=1
log "$NAME start, junk $JUNK, ks $KS, extra '$EXTRA', state $STATE, hp $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
t=$(date +%s)
timeout --signal=TERM $LIMIT nice -n 10 $PY -u anm_run.py $SCR $OUT/$NAME --state $STATE $F --ks $KS --keep_plan 1 --steps 1 $EXTRA \
  >> $OUT/$NAME.log 2>&1
rc=$?
log "$NAME exit $rc wall $(( $(date +%s) - t )) s (124 is the ${LIMIT} s limit)"
exit $rc
