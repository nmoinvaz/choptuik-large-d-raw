#!/usr/bin/env bash
# #268 second part: the octo-double load check of anm_run.py (the base polish of a start state) on each I19-win2 crawl state that has a row
# in delta_all.csv, with the crawl's own options, --state = that state and --steps 0 (no step beyond it). From hp/ of the worktree
# D:\choptuik-t126 (the one that ran #19, hp code equal to e743608 and c691ae3), venv-t126 (Python 3.12.8). Normal priority, 8 threads.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I268-win2
cd /d/choptuik-t126/hp || exit 9
export PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
STATES=${1:-"214.6000 214.7000 214.8000 214.9000 215.0000 215.0250 215.0312"}
echo "start $(stamp), states [$STATES]" >> $R/exits.txt
for d in $STATES; do
  t=$(date +%s)
  "$PY" -u anm_run.py $RAW $R/out_D$d --state I19-win2/crawl/anm_pin3_D$d.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
     --h_max 0.1 --steps 0 --D_max 220 --threads 8 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
     --save_pred 1 > $R/load_D$d.log 2>&1
  echo "D$d exit $? wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt
done
echo "done $(stamp)" >> $R/exits.txt
