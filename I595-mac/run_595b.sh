#!/usr/bin/env bash
# #595, the coordinator's step first: a direct base polish of the re-planned D 215.00 and D 225.13 states with main's
# anm_run.py (d020d58, the od gate of 62bc52a; crawlJ's chain flags with --steps 0 --save_base 1 --tol_od 1e-60), on
# cadcaf1's wheel (exact rows) and, as the control, on main's old wheel (rounded rows); then the traces at D 235, 240
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
C2=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
MAINHP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i589/mainhp/hp
MYHP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp
R=$RAW/I595-mac
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt; }
polish() {   # name, kernel path ('' for main's old wheel), state, held fit
  local n=$1 k=$2 st=$3 fit=$4
  cd $MAINHP || exit 9
  PYTHONPATH=$k $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/$n.log
  log "$n start"
  PYTHONPATH=$k nice -n 10 $PY -u anm_run.py $RAW $R/$n --state $st --kfreeze 3 --held_fit $fit --N 24 --eps 1e-14 \
    --h_max 1.0 --steps 0 --D_max 400 --threads 4 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 \
    --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 \
    >> $R/$n.log 2>&1
  log "$n exit $?"
}
trace() {
  local n=$1; shift
  cd $MYHP || exit 9
  PYTHONPATH=$C2 $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/$n.log
  log "$n start"
  PYTHONPATH=$C2 nice -n 10 $PY -u held_homotopy.py "$@" --rule 2 --threads 4 --hours 1.5 --ladder 0:90:2 >> $R/$n.log 2>&1
  log "$n exit $?"
}
polish polish_c2_s215   $C2 I589-mac/s215.npz data/held_fit_d6.json
polish polish_main_s215 ""  I589-mac/s215.npz data/held_fit_d6.json
polish polish_c2_s225   $C2 I589-mac/s225.npz data/held_fit.json
polish polish_main_s225 ""  I589-mac/s225.npz data/held_fit.json
trace real235 $RAW I589-mac/s235.npz $R/real235 --mode real
trace real240 $RAW I589-mac/s240.npz $R/real240 --mode real
