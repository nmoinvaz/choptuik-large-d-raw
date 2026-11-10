#!/usr/bin/env bash
# #268 second part, second driver: the same command as run_i268.sh for the states given, with THREADS threads, skipping a state whose
# load_D<D>.log already exists (another driver took it). Usage: run_i268_par.sh THREADS "214.7000 214.8000 214.9000" (or in reverse order).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I268-win2
cd /d/choptuik-t126/hp || exit 9
export PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
TH=$1
echo "driver start $(stamp), threads $TH, states [$2]" >> $R/exits.txt
for d in $2; do
  if [ -e $R/load_D$d.log ]; then echo "D$d skipped by this driver (log exists) $(stamp)" >> $R/exits.txt; continue; fi
  : > $R/load_D$d.log
  t=$(date +%s)
  "$PY" -u anm_run.py $RAW $R/out_D$d --state I19-win2/crawl/anm_pin3_D$d.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
     --h_max 0.1 --steps 0 --D_max 220 --threads $TH --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
     --save_pred 1 > $R/load_D$d.log 2>&1
  echo "D$d exit $? wall $(( $(date +%s) - t ))s threads $TH $(stamp)" >> $R/exits.txt
done
echo "driver done [$2] $(stamp)" >> $R/exits.txt
