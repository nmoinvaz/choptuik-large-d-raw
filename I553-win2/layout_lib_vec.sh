# sourced by lane_553.sh (after layout_lib.sh)
VECPY=/d/choptuik-large-d-raw/I553-win2/near_null_vec.py
# layout_vec FOLDER LANE TAG NODES   renode, then near_null_vec and near_null_eq on the new start
layout_vec() {
  local folder=$1 lane=$2 tag=$3 nodes=$4
  local R=$RAW/$folder
  step $folder $lane renode_$tag $MAIN 0 renode_$tag.log "$PY" -u renode_o.py $RAW $J $folder/renode_${tag}_D242.3642.npz --nodes $nodes --threads 2
  nn_vec $folder $lane $tag $folder/renode_${tag}_D242.3642.npz
  step $folder $lane near_null_eq_$tag $EQ 0 eq_$tag.log "$PY" -u near_null_eq.py $RAW $folder/renode_${tag}_D242.3642.npz --plant=7 --threads=2 --json=$R/eq_$tag.json
}
# nn_vec FOLDER LANE TAG STATE   near_null_vec.py on a state (the existing layouts too)
nn_vec() {
  local folder=$1 lane=$2 tag=$3 state=$4
  local R=$RAW/$folder
  step $folder $lane near_null_vec_$tag $MAIN 0 nnv_$tag.log "$PY" -u $VECPY $RAW $state --k=4 --threads=2 --json=$R/nnv_$tag.json --vec=$R/vec_$tag.npz
}
