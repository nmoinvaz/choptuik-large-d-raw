#!/usr/bin/env bash
# #461 crawlG: a second chain from the first state past the wall, crawlB2/anm_pin3_D215.1312.npz (D 215.13125), at main cc6d51b with today's options from its first step:
# --od_junk 0 --base_polish 0 --held_o 1 --reseed_o 3 --h_max 1.0 --steps 400 --D_max 400 --qd_it 40, the rest as crawlF. Output crawlG, log crawlG.log, 18 threads, Normal priority,
# no affinity, venv-t126, by the coordinator's order of 2026-11-10 21:31 UTC (crawlF stopped 21:32:09 UTC at D 240.15625). The 30 h cap counts from this start.
# The first step is a restart step from a state without a plan (judge from the second); every state it saves carries its plan.
# Reading rule: report at once the first step with more than 6 Newton steps, any lam below 1, any refusal, and the series line whenever |z_N| is above 1e-27 or the fourth ratio below 100.
# Hourly table: Delta of each state beside the first chain's Delta at the same D (215.13125 + k up to 226.13125), they must agree to about 1e-16.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/crawlB2/anm_pin3_D215.1312.npz
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "cc6d51b" ] || { echo "worktree D:/choptuik-i446 is not at cc6d51b" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part G start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlG --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlG.log 2>&1
rc=$?
echo "part G anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
