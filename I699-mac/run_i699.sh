#!/bin/bash
# I699-mac: corrector starts on #553's x_last 0.77 layout and #543's 0.80 layout (anm_run.py --steps 1 --save_dz0 1, on
# #677's flags with --base_polish 0), each stopped once its dz0 is saved; then reduced_cubic.py rows, its plant and the
# plant's two controls first, at both starts, and rowsum. Run from the code checkout's hp/ as
#   bash run_i699.sh RAW OUT
# RAW a clone of the raw-data repository (the inputs), OUT this folder inside it. One process at a time, 2 threads.
RAW=$1
OUT=$2
PY=${PY:-/Users/nathan/venv-314/bin/python3}
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
rev=$(git rev-parse --short=8 HEAD)
start() {   # name, the re-noded state (relative to RAW)
  local name=$1 st=$2
  mkdir -p "$OUT/$name"
  echo "$name start $(stamp) $rev" >> "$OUT/exits.txt"
  nice -n 10 "$PY" -u anm_run.py "$RAW" "$OUT/$name" --state "$st" --kfreeze 3 --held_fit data/held_fit.json --N 24 \
    --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 2 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 \
    --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
    --save_dz0 1 --a0 0.476837158203125 --od_accept own --base_polish 0 > "$OUT/$name.log" 2>&1 &
  local pid=$!
  while kill -0 $pid 2>/dev/null; do
    if grep -q "saved the start and first step" "$OUT/$name.log"; then
      kill $pid
      echo "$name stopped after its dz0 was saved $(stamp)" >> "$OUT/exits.txt"
      break
    fi
    sleep 20
  done
  wait $pid
  echo "$name exit $? $(stamp)" >> "$OUT/exits.txt"
}
one() {   # name, then the arguments of reduced_cubic.py
  local name=$1
  shift
  echo "$name start $(stamp) $rev" >> "$OUT/exits.txt"
  nice -n 10 "$PY" -u reduced_cubic.py "$@" --json="$OUT/$name.json" > "$OUT/$name.log" 2>&1
  echo "$name exit $? $(stamp)" >> "$OUT/exits.txt"
}
one rows_planted rows planted
one rows_planted_mut_quadA rows planted --mutate=quadA
one rows_planted_mut_parity rows planted --mutate=parity
start l077 I553-win2/renode_last077_D242.3642.npz
start l080 I543-win2/renode_last080_D242.3642.npz
rel() { local f; f=$(ls "$OUT/$1"/dz0_pin3_*.npz 2>/dev/null | head -1); echo "${f#$RAW/}"; }
D77=$(rel l077)
D80=$(rel l080)
[ -n "$D77" ] && one rows_l077 rows "$RAW" "$D77" I553-win2/renode_last077_D242.3642.npz --threads=2
[ -n "$D80" ] && one rows_l080 rows "$RAW" "$D80" I543-win2/renode_last080_D242.3642.npz --threads=2
"$PY" reduced_cubic.py rowsum "$OUT"/rows_l0*.json > "$OUT/rowsum.txt" 2>&1
echo "rowsum exit $? $(stamp)" >> "$OUT/exits.txt"
echo "all done $(stamp)" >> "$OUT/exits.txt"
