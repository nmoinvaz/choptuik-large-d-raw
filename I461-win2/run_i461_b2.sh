#!/usr/bin/env bash
# #461 part B2: part B's command (run_i461_b.sh) with the base-polish rule of commit d84cc51 (branch fix/base-polish-not-adopted, one commit on
# main 62e725d, hp/anm_run.py only), from hp/ of the worktree D:\choptuik-i446 detached at d84cc51. Output folder crawlB2, log crawlB2.log.
# No --base_adopt (its default 0 is the rule under test). venv-t126, 18 threads, Normal priority, no affinity.
# The log must print "base polish not adopted (max|F| 4.4e-36 -> 1.5e-18): the stored state is the base" after the polish lines, and a step 0 line
# "pivots 7.2e-16..2.3e+30, |z_1| 4.37e-04, |z_N| 2.37e-30, ratios 2-5 274.8 247.7 236.2 229.7, a_max 3.414" before the first attempt.
# Stop rules: three halvings without an accepted step ("stopped: no convergence after three halvings"), a 6 h cap from the start (watched by a
# separate loop, not killed here), the hang rule (no log line for 20 min with one core busy).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "d84cc51" ] || { echo "worktree D:/choptuik-i446 is not at d84cc51" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part B2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlB2 --state I19-win2/crawl/anm_pin3_D215.0312.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.1 --steps 4 --D_max 220 --threads 18 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawlB2.log 2>&1
rc=$?
echo "part B2 anm_run --steps 4 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
