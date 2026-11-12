#!/usr/bin/env bash
# #562 (approved by the coordinator): after pid $1 (#595's polish_main_s225) ends, a direct base polish of crawlJ's
# D 242.3642 state on cadcaf1 (exact rows; crawlJ's flags, its stored plan, --tol_od 1e-60); if it converges, the
# renode of the polished base to 0.3, 0.4, 0.5, 0.6, 0.975 (its check and the sign control), near_null and the probe
# there; then #595's remaining polishes at D 235.13 and 240.03 on both kernels
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
C2=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
MAINHP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i589/mainhp/hp
MYHP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp
R562=$RAW/I562-mac
R595=$RAW/I595-mac
log() { echo "$2 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $1/exits.txt; }
while kill -0 "$1" 2>/dev/null; do sleep 10; done
log $R595 "polish_main_s225 ended (its parent script was stopped; its exit is read from its log)"
polish() {   # folder, name, kernel path ('' for main's old wheel), state, held fit
  local R=$1 n=$2 k=$3 st=$4 fit=$5
  cd $MAINHP || exit 9
  PYTHONPATH=$k $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/$n.log
  log $R "$n start"
  PYTHONPATH=$k nice -n 10 $PY -u anm_run.py $RAW $R/$n --state $st --kfreeze 3 --held_fit $fit --N 24 --eps 1e-14 \
    --h_max 1.0 --steps 0 --D_max 400 --threads 4 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 \
    --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --save_base 1 \
    >> $R/$n.log 2>&1
  log $R "$n exit $?"
}
polish $R562 polish_c2_s242 $C2 I461-win2/crawlJ/anm_pin3_D242.3642.npz data/held_fit.json
B=I562-mac/polish_c2_s242/base_pin3_D242.3642.npz
conv=$($PY -c "import json, numpy as np; m = json.loads(str(np.load('$RAW/$B')['meta'])); bp = m.get('base_polish', {}); print(int(bool(bp.get('converged')) and bp['max_F'][1] < 1e-60))" 2>/dev/null)
if [ "$conv" = "1" ]; then
  cd $MYHP || exit 9
  PYTHONPATH=$C2 nice -n 10 $PY -u renode_o.py $RAW $B I562-mac/c2_renode_0975.npz --nodes 0.3,0.4,0.5,0.6,0.975 --threads 4 > $R562/c2_renode_0975.log 2>&1
  log $R562 "c2_renode_0975 exit $? (check must pass)"
  PYTHONPATH=$C2 nice -n 10 $PY -u renode_o.py $RAW $B I562-mac/c2_renode_0975_mut.npz --nodes 0.3,0.4,0.5,0.6,0.975 --threads 4 --mutate sign > $R562/c2_renode_0975_mut.log 2>&1
  log $R562 "c2_renode_0975_mut exit $? (must be nonzero)"
  cd $MAINHP || exit 9
  PYTHONPATH=$C2 nice -n 10 $PY -u near_null.py $RAW I562-mac/c2_renode_0975.npz --threads=4 --json=$R562/c2_nn_renode_0975.json > $R562/c2_nn_renode_0975.log 2>&1
  log $R562 "c2_nn_renode_0975 exit $?"
  cd $MYHP || exit 9
  PYTHONPATH=$C2 nice -n 10 $PY -u held_homotopy.py $RAW I562-mac/c2_renode_0975.npz $R562/c2_probe_renode_0975 --mode real --threads 4 --probe_only 1 --ladder 0:90:2 > $R562/c2_probe_renode_0975.log 2>&1
  log $R562 "c2_probe_renode_0975 exit $?"
else
  log $R562 "polish_c2_s242: no converged base (max|F| < 1e-60); no renode"
fi
polish $R595 polish_c2_s235   $C2 I589-mac/s235.npz data/held_fit.json
polish $R595 polish_main_s235 ""  I589-mac/s235.npz data/held_fit.json
polish $R595 polish_c2_s240   $C2 I589-mac/s240.npz data/held_fit.json
polish $R595 polish_main_s240 ""  I589-mac/s240.npz data/held_fit.json
