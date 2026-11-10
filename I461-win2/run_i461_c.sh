#!/usr/bin/env bash
# #461 part C, the pilot of the cure: crawlB5's command from its last saved state with --held_o 1 --reseed_o 3 --base_polish 0 and --steps 3, at commit 9e5fd9f
# (branch feat/reseed-od-refine, hp/anm_run.py octo_corrector.py pinning.py reseed.py only), worktree D:\choptuik-i446 detached at 9e5fd9f, by the coordinator's
# order of 2026-11-10 19:33 UTC (crawlB5 stopped at 19:34:48 UTC). Output crawlC, log crawlC.log, 18 threads, Normal priority, no affinity, venv-t126.
# Reading rule (the coordinator, written before the run): pass = each of the 3 steps accepted at a 1.0 with at most 6 Newton steps and lam 1 at every iteration;
# fail = an a 1.0 attempt refused, or an accepted step above 12 Newton steps (let the run end, report every attempt's Newton lines); 7 to 12 steps or a lam
# below 1 = report the lines, the coordinator decides. The log must print "base polish skipped (--base_polish 0): the stored state is the base" and a step 0
# series line with |z_N| below 1e-27 and a_max above 3, and after each "re-seeded (ok)" a line "horizon data refined in octo-double, rung max|R| a -> b -> c -> d"
# whose last number is below 1e-50. If the pilot passes: crawlD from crawlC's last state, --steps 400, a new 30 h cap.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlB5/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "9e5fd9f" ] || { echo "worktree D:/choptuik-i446 is not at 9e5fd9f" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part C start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlC --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 3 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlC.log 2>&1
rc=$?
echo "part C anm_run --steps 3 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
