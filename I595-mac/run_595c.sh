#!/usr/bin/env bash
# #595, continued: after polish_main_s215 (pid $1) ends, the base polishes at D 225.13, 235.13 and 240.03 on cadcaf1
# (exact rows) and on main's old wheel (rounded rows, the control); same flags as run_595b.sh
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
C2=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
MAINHP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i589/mainhp/hp
R=$RAW/I595-mac
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt; }
while kill -0 "$1" 2>/dev/null; do sleep 10; done
log "polish_main_s215 ended (its parent script was stopped; its exit is read from its log)"
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
polish polish_c2_s225   $C2 I589-mac/s225.npz data/held_fit.json
polish polish_main_s225 ""  I589-mac/s225.npz data/held_fit.json
polish polish_c2_s235   $C2 I589-mac/s235.npz data/held_fit.json
polish polish_main_s235 ""  I589-mac/s235.npz data/held_fit.json
polish polish_c2_s240   $C2 I589-mac/s240.npz data/held_fit.json
polish polish_main_s240 ""  I589-mac/s240.npz data/held_fit.json
