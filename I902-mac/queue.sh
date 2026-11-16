#!/bin/bash
# #902: the model's ln f, then near_null.py at the stored z with the horizon series summed to ks 130, 160, 200, 250 at
# #603's states D 253.80 (first, the hardest: ks 250 as the pilot, then 130 and the control --mutate=ks), 249.01 and
# 237.13, and at D 60 (the control); then sigma.py. Waits for I875-mac's queue: one process at a time. Stops if the
# pilot does not run to its end.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I902-mac
WT=/Users/nathan/Source/choptuik-large-d-902
PY=/Users/nathan/venv-314/bin/python3
st() {   # the state of each D (bash 3.2: no associative arrays)
  case $1 in
    253) echo I603-win2/chain_nat/anm_pin3_D253.8043.npz ;;
    249) echo I603-win2/chain/anm_pin3_D249.0113.npz ;;
    237) echo I603-win2/chain/anm_pin3_D237.1312.npz ;;
    60) echo I611-win/kf13_D60_D60.001952.npz ;;
  esac
}
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
nn() { d=$1; K=$2; shift 2; ./run.sh nn_D${d}_ks$K$tag near_null.py $R $(st $d) --k=6 --its=16 --threads=3 --ks=$K \
  --json=$O/nn_D${d}_ks$K$tag.json "$@"; }
until [ -f $R/I875-mac/queue.done ]; do sleep 60; done
{ echo "== model $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $WT at $(git -C $WT rev-parse --short=8 HEAD)"
  (cd $WT && OPENBLAS_NUM_THREADS=1 nice -n 10 $PY -u solver/factored_horizon_sympy.py model); echo "exit $?"; } \
  > $O/model.log 2>&1
tag=""
nn 253 250 --save_v=$O/V_D253_ks250.npy
if ! grep -q "^check:" $O/nn_D253_ks250.log; then echo "pilot did not finish: stopped" >> queue.log; exit 1; fi
nn 253 130 --save_v=$O/V_D253_ks130.npy
tag=_mutks; nn 253 250 --mutate=ks; tag=""
for K in 160 200; do nn 253 $K --save_v=$O/V_D253_ks$K.npy; done
for d in 249 237 60; do
  for K in 130 160 200 250; do nn $d $K --save_v=$O/V_D${d}_ks$K.npy; done
done
chk sigma_selftest sigma.py --selftest
chk sigma sigma.py $O
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
