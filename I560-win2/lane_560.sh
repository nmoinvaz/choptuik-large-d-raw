#!/usr/bin/env bash
# #560: crawlG D 232.6312 and crawlI D 237.1312 re-noded to last node 0.8, near_null on each, the reproducibility run on #543's D 242.36 layout, and the controls.
. /d/choptuik-large-d-raw/I560-win2/layout_lib.sh
F=I560-win2; R=$RAW/$F
rn() {   # rn TAG SRC NODES : renode_o on a source state
  step $F Q renode_$1 $MAIN 0 renode_$1.log "$PY" -u renode_o.py $RAW $2 $F/renode_$1_80.npz --nodes $3 --threads 2
}
nnq() {  # nnq TAG STATE : near_null
  step $F Q near_null_$1 $MAIN 0 nn_$1.log "$PY" -u near_null.py $RAW $2 --k=4 --threads=2 --json=$R/nn_$1.json
}
rn D232 I461-win2/crawlG/anm_pin3_D232.6312.npz 0.3,0.4,0.5,0.6,0.8
nnq D232 $F/renode_D232_80.npz
rn D237 I461-win2/crawlI/anm_pin3_D237.1312.npz 0.3,0.4,0.5,0.6,0.8
nnq D237 $F/renode_D237_80.npz
nnq D242 I543-win2/renode_last080_D242.3642.npz
step $F Q renode_D237_mut_sign $MAIN 1 renode_D237_mut.log "$PY" -u renode_o.py $RAW I461-win2/crawlI/anm_pin3_D237.1312.npz $F/renode_D237_mut.npz --nodes 0.3,0.4,0.5,0.6,0.8 --threads 2 --mutate sign
step $F Q near_null_D232_mut_sigma $MAIN 1 nn_D232_ctl_sigma.log "$PY" -u near_null.py $RAW $F/renode_D232_80.npz --k=4 --threads=2 --mutate=sigma
echo "lane #560 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
