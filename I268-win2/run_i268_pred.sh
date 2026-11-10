#!/usr/bin/env bash
# #268 second part, extra check: the same load check on the crawl's saved PREDICTIONS (pred_pin3_D<D>.npz, --save_pred 1), i.e. the start the
# crawl's own corrector had at each accepted step, instead of the converged states. Usage: run_i268_pred.sh THREADS "214.6000 ..." (one process per state).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I268-win2
cd /d/choptuik-t126/hp || exit 9
export PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
TH=$1
echo "pred driver start $(stamp), threads $TH, states [$2]" >> $R/exits.txt
for d in $2; do
  t=$(date +%s)
  "$PY" -u anm_run.py $RAW $R/out_pred_D$d --state I19-win2/crawl/pred_pin3_D$d.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
     --h_max 0.1 --steps 0 --D_max 220 --threads $TH --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
     --save_pred 1 > $R/load_pred_D$d.log 2>&1
  echo "pred D$d exit $? wall $(( $(date +%s) - t ))s threads $TH $(stamp)" >> $R/exits.txt
done
echo "pred driver done [$2] $(stamp)" >> $R/exits.txt
