#!/usr/bin/env bash
# #461 part B: the crawl's command from I19-win2/crawl/anm_pin3_D215.0312.npz (D 215.03125) with --steps 4, from hp/ of the worktree D:\choptuik-i446
# (detached at d9e7f78, so the fixed hp/reseed.py is the one imported), venv-t126 (Python 3.12.8), 18 threads, Normal priority, no affinity.
# Stop rules: the crawl's three halvings without an accepted step (anm_run prints "stopped: no convergence after three halvings"), a 6 h cap
# (watched by a separate loop, not killed here), the hang rule (no log line for 20 min with one core busy).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
cd /d/choptuik-i446/hp || exit 9
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part B start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlB --state I19-win2/crawl/anm_pin3_D215.0312.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.1 --steps 4 --D_max 220 --threads 18 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawlB.log 2>&1
rc=$?
echo "part B anm_run --steps 4 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
