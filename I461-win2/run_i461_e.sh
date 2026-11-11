#!/usr/bin/env bash
# #461 pilot E: crawlD's command from crawlD's last saved state with --od_junk 4 and --steps 3, at main cc6d51b ("a restarted chain keeps the plan its state was
# converged under": hp/anm_run.py only), worktree D:\choptuik-i446 detached at cc6d51b, by the coordinator's order of 2026-11-10 20:38 UTC (crawlD stopped 20:39:03 UTC
# because its second step stalled at lam 0.0078 with |F| 3.6e-22). Output crawlE, log crawlE.log, 18 threads, Normal priority, no affinity, venv-t126.
# Reading rule (the coordinator, written before the run): the first "od:" line of the first attempt decides. If it reads "0 junk directions frozen" stop pilot E at once and
# start crawlD again from the same state with --od_junk 0 and --h_max 0.35 (output crawlD2), and report the line. If it freezes 1 or more: report the line (count, sigma, how
# many weak ones kept), let the 3 steps run and report each step's Newton count, its convergence line in full and Delta against the degree-5 extrapolation.
# Pass: each step accepted at a 0.7 in at most 6 Newton steps. Fail: a refusal, or more than 12 steps. The first step is again a restart step: judge from the second.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlD/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "cc6d51b" ] || { echo "worktree D:/choptuik-i446 is not at cc6d51b" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part E start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlE --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.7 --steps 3 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlE.log 2>&1
rc=$?
echo "part E anm_run --steps 3 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
