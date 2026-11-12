# sourced by the lanes of #566 after layout_lib.sh
F=I566-win2
NNV=/d/choptuik-large-d-raw/I566-win2/near_null_vec.py
EQV=/d/choptuik-large-d-raw/I566-win2/near_null_eq_vec.py
R=$RAW/$F
# vecs LANE TAG STATE PLANT   near_null_vec then near_null_eq_vec on a state (PLANT=1: --plant=7)
vecs() {
  local lane=$1 tag=$2 state=$3 plant=$4
  step $F $lane near_null_vec_$tag $MAIN 0 nnv_$tag.log "$PY" -u $NNV $RAW $state --k=4 --threads=2 --json=$R/nnv_$tag.json --vec=$R/vec_$tag.npz
  local pl=""; [ "$plant" = 1 ] && pl="--plant=7"
  step $F $lane near_null_eq_vec_$tag $EQ 0 eqv_$tag.log "$PY" -u $EQV $RAW $state --threads=2 $pl --json=$R/eqv_$tag.json --vec=$R/veq_$tag.npz
}
# newlayout LANE TAG NODES : renode then vecs with the planted check
newlayout() {
  step $F $1 renode_$2 $MAIN 0 renode_$2.log "$PY" -u renode_o.py $RAW $J $F/renode_$2_D242.3642.npz --nodes $3 --threads 2
  vecs $1 $2 $F/renode_$2_D242.3642.npz 1
}
