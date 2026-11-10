#!/usr/bin/env bash
# #287: the first step of the I19-win2 crawl past D 214.5, reproduced on win2's new firmware. The crawl's own command (I19-win2/README.md)
# with --steps 1, from T138-win2/chain_o/anm_pin3_D214.5000.npz. From hp/ of the worktree D:\choptuik-t126 (the one that ran #19), venv-t126
# (Python 3.12.8), 18 threads like the crawl, Normal priority, no affinity.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I287-win2
cd /d/choptuik-t126/hp || exit 9
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawl1 --state T138-win2/chain_o/anm_pin3_D214.5000.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.1 --steps 1 --D_max 220 --threads 18 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawl1.log 2>&1
rc=$?
echo "anm_run --steps 1 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
