#!/usr/bin/env bash
# #537 lane B: last node 0.7 -> 0.72, with the renode control and the near_null control.
. /d/choptuik-large-d-raw/I537-win2/lane_common.sh
step B renode_last072 $MAIN 0 renode_last072.log "$PY" -u renode_o.py $RAW $J I537-win2/renode_last072_D242.3642.npz --nodes 0.3,0.4,0.5,0.6,0.72 --threads 2
step B renode_last072_mut_sign $MAIN 1 renode_last072_mut.log "$PY" -u renode_o.py $RAW $J I537-win2/renode_last072_mut.npz --nodes 0.3,0.4,0.5,0.6,0.72 --threads 2 --mutate sign
step B near_null_last072 $MAIN 0 nn_last072.log "$PY" -u near_null.py $RAW I537-win2/renode_last072_D242.3642.npz --k=4 --threads=2 --json=$R/nn_last072.json
step B near_null_eq_last072 $EQ 0 eq_last072.log "$PY" -u near_null_eq.py $RAW I537-win2/renode_last072_D242.3642.npz --plant=7 --threads=2 --json=$R/eq_last072.json
step B near_null_last072_mut_sigma $MAIN 1 nn_last072_ctl_sigma.log "$PY" -u near_null.py $RAW I537-win2/renode_last072_D242.3642.npz --k=4 --threads=2 --mutate=sigma
echo "lane B done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
