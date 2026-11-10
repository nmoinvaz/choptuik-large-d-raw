#!/usr/bin/env bash
# #296: the rest of the I19-win2 crawl (D 214.6 to 215.03125), the crawl's own command with --steps 40, from T138-win2/chain_o/anm_pin3_D214.5000.npz.
# From hp/ of the worktree D:\choptuik-t126 (the one that ran #19), venv-t126 (Python 3.12.8), 18 threads like the crawl, Normal priority, no affinity.
# Waits for #295 step 1 (3 processes) to end, so that the 18 threads have the machine.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I296-win2
until grep -q 'step 1 amp_flint_par.* exit' $RAW/I295-win2/exits.txt; do sleep 15; done
cd /d/choptuik-t126/hp || exit 9
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawl --state T138-win2/chain_o/anm_pin3_D214.5000.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.1 --steps 40 --D_max 220 --threads 18 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawl.log 2>&1
rc=$?
echo "anm_run --steps 40 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
