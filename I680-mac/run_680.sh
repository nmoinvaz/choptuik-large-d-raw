#!/bin/bash
# I680-mac: the base polish of T138-win2's D 80 state on the rounded projector's rows (venv-314's installed hpkernel,
# the build of 2026-11-08/09 before #523) and on the exact rows (main 3c35f0c's kernel, i599/site2), as #595 made its
# rows (crawlJ's chain flags with --steps 0 --save_base 1 --tol_od 1e-60); the rounded polish twice, the control. Then
# delta_diff.py. Run from the code checkout's hp/ as: bash run_680.sh RAW OUT. One process at a time, 2 threads.
RAW=$1
OUT=$2
PY=${PY:-/Users/nathan/venv-314/bin/python}
EXACT=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
ST=T138-win2/chain/anm_pin3_D80.0000.npz
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
rev=$(git rev-parse --short=8 HEAD)
polish() {   # name, kernel path ('' for the installed one)
  local n=$1 k=$2
  PYTHONPATH=$k $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > "$OUT/$n.log"
  echo "$n start $(stamp) $rev" >> "$OUT/exits.txt"
  PYTHONPATH=$k nice -n 10 $PY -u anm_run.py "$RAW" "$OUT/$n" --state $ST --kfreeze 3 --held_fit data/held_fit.json \
    --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --D_max 400 --threads 2 --corrector od --tol_od 1e-60 --qd_it 12 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 \
    --save_pred 1 --save_base 1 >> "$OUT/$n.log" 2>&1
  echo "$n exit $? $(stamp)" >> "$OUT/exits.txt"
}
polish polish_rounded ""
polish polish_exact "$EXACT"
polish polish_rounded2 ""
B=base_pin3_D80.0000.npz
$PY delta_diff.py "$RAW" $ST I680-mac/polish_exact/$B I680-mac/polish_rounded/$B > "$OUT/delta_diff_D80.log" 2>&1
echo "delta_diff_D80 exit $? $(stamp)" >> "$OUT/exits.txt"
$PY delta_diff.py "$RAW" $ST I680-mac/polish_rounded2/$B I680-mac/polish_rounded/$B > "$OUT/delta_diff_D80_control.log" 2>&1
echo "delta_diff_D80_control exit $? $(stamp)" >> "$OUT/exits.txt"
echo "all done $(stamp)" >> "$OUT/exits.txt"
