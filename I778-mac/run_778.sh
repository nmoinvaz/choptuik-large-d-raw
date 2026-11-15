#!/bin/bash
# I778-mac: #742's attempt N (natural test, a = 1 from D 117) rebuilt through anm_run to Newton step 1 on the pre-#523
# build (venv-314's installed hpkernel), then logcmp against N.log, probe's theta with the weak share, and weak.
# Run from the code checkout's hp/ as: bash run_778.sh RAW OUT. One process at a time, 4 threads.
RAW=$1
OUT=$2
PY=${PY:-/Users/nathan/venv-314/bin/python}
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
unset PYTHONPATH
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
IT=$OUT/R/crawl_iter_D118.0000_s1.npz
run anm anm "$RAW" "$OUT/R" --stop 1 --attempts 1 --state I742-win/L/anm_pin13_D117.0000.npz --kfreeze 13 --N 24 \
  --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 \
  --reseed_o 3 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --elim_switch 0 --steps 1 --h_max 1.0 --a0 1.0 \
  --od_accept natural --threads 4
N=$RAW/I742-win/logs/N.log
run logcmp_base logcmp "$OUT/anm.log" $N --anchor "the base keeps its stored plan" --n 5
run logcmp_step0 logcmp "$OUT/anm.log" $N --anchor "step 0: D 117.0" --n 11
run logcmp_step1 logcmp "$OUT/anm.log" $N --anchor "on 1 trial lam 1:" --n 3
run logcmp_control logcmp "$OUT/anm.log" $N --anchor "step 0: D 117.0" --n 11 --mutate digit
run probe probe "$RAW" "$IT" --out "$OUT/probe" --threads 4 --arms none --theta 1 --weak 4
run weak weak "$RAW" --iter "$IT" --lams 0,1 --w 4 --threads 4 --out "$OUT/weak.jsonl"
echo "all done $(stamp)" >> "$OUT/exits.txt"
