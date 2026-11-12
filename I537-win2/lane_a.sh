#!/usr/bin/env bash
# #537 lane A: first node 0.3 -> 0.35, then the baseline.
. /d/choptuik-large-d-raw/I537-win2/lane_common.sh
step A renode_first035 $MAIN 0 renode_first035.log "$PY" -u renode_o.py $RAW $J I537-win2/renode_first035_D242.3642.npz --nodes 0.35,0.4,0.5,0.6,0.7 --threads 2
step A near_null_first035 $MAIN 0 nn_first035.log "$PY" -u near_null.py $RAW I537-win2/renode_first035_D242.3642.npz --k=4 --threads=2 --json=$R/nn_first035.json
step A near_null_eq_first035 $EQ 0 eq_first035.log "$PY" -u near_null_eq.py $RAW I537-win2/renode_first035_D242.3642.npz --plant=7 --threads=2 --json=$R/eq_first035.json
step A near_null_base $MAIN 0 nn_base.log "$PY" -u near_null.py $RAW $J --k=4 --threads=2 --json=$R/nn_base.json
step A near_null_eq_base $EQ 0 eq_base.log "$PY" -u near_null_eq.py $RAW $J --plant=7 --threads=2 --json=$R/eq_base.json
echo "lane A done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
