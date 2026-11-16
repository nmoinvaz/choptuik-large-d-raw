#!/bin/bash
# #902, the queue's second part (queue.sh ran the model and the ks 250 pilot at D 253.80, then was stopped at 05:20
# UTC to add near_null.py --jv=od): D 253.80 at ks 130 with --jv=both (the octo-double J v_1 against the 140-digit
# one), the control --mutate=ks, ks 160 and 200; then D 249.01, 237.13 and 60 at ks 130, 160, 200, 250 with
# --jv=od; then sigma.py. One process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I902-mac
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
tag=""
nn 253 130 --jv=both --save_v=$O/V_D253_ks130.npy
tag=_mutks; nn 253 250 --mutate=ks --jv=od; tag=""
for K in 160 200; do nn 253 $K --jv=od --save_v=$O/V_D253_ks$K.npy; done
for d in 249 237 60; do
  for K in 130 160 200 250; do nn $d $K --jv=od --save_v=$O/V_D${d}_ks$K.npy; done
done
chk sigma_selftest sigma.py --selftest
chk sigma sigma.py $O
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
