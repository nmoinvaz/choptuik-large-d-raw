#!/bin/bash
# I779-mac: on main's build (i599/site2), #742's own-test attempts from the D 117 state (polished there by anm_run) at
# a = 1, 1/2 and 1/4 to Newton step 1 (crawl_probe.py anm --stop 1 --attempts 3), then each iterate's root by fixrun.
# junk_err.py runs after, with W read from anm.log (README). Run from the code checkout's hp/ as: bash run_779.sh RAW OUT.
RAW=$1
OUT=$2
PY=${PY:-/Users/nathan/venv-314/bin/python}
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
rev=$(git rev-parse --short=8 HEAD)
run() {   # name, then crawl_probe.py's arguments
  local n=$1
  shift
  $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > "$OUT/$n.log"
  echo "$n start $(stamp) $rev" >> "$OUT/exits.txt"
  nice -n 10 $PY -u crawl_probe.py "$@" >> "$OUT/$n.log" 2>&1
  echo "$n exit $? $(stamp)" >> "$OUT/exits.txt"
}
run anm anm "$RAW" "$OUT/R" --stop 1 --attempts 3 --state I742-win/L/anm_pin13_D117.0000.npz --kfreeze 13 --N 24 \
  --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 \
  --reseed_o 3 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --elim_switch 0 --steps 1 --h_max 1.0 --a0 1.0 \
  --threads 4
for D in 118.0000 117.5000 117.2500; do
  run fix_$D fixrun "$RAW" "$OUT/R/crawl_iter_D${D}_s1.npz" --out "$OUT/fix" --threads 4 --switch 0 --accept own --steps 8 --tol 1e-60
done
echo "all done $(stamp)" >> "$OUT/exits.txt"
