#!/usr/bin/env bash
# #461 crawlF: the chain from pilot E's accepted state with 0 junk directions frozen (the a 0.35 step to D 239.80625), at main cc6d51b, crawlD's command with --od_junk 0 and
# --h_max 0.35, --steps 400, output crawlF, log crawlF.log, 18 threads, Normal priority, no affinity, venv-t126, by the coordinator's order of 2026-11-10 21:02 UTC (it replaces crawlD2).
# Pilot E was stopped at 21:03:00 UTC because its freeze (1 direction at a 0.7) can only hurt. The first test of cc6d51b's stored plan: the log must print
# "the base keeps its stored plan (N steps)" right after the start, and the first step's first |dz| must be far below the 1e-15 of a restart step.
# Reading rule: at a 0.35 expect 10 to 20 Newton steps with runs of lam 0.5, accepted; report at once a refusal, a lam below 0.25, or more than 25 steps.
# Series rule: stop and report if |z_N| is above 1e-24 or a_max is below 2.0; warn once under a_max 2.5. The 30 h cap counts from this start.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlE/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "cc6d51b" ] || { echo "worktree D:/choptuik-i446 is not at cc6d51b" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part F start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlF --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.35 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlF.log 2>&1
rc=$?
echo "part F anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
