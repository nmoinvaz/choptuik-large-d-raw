#!/usr/bin/env bash
# #461 part D, the chain with the cure: the pilot's command (run_i461_c.sh) from crawlC's last saved state with --steps 400 and --h_max 0.7, at commit 9e5fd9f
# (branch feat/reseed-od-refine), worktree D:\choptuik-i446 detached at 9e5fd9f, by the coordinator's orders of 2026-11-10 19:56 and 20:01 UTC (pilot ended 20:02:43 UTC).
# Output crawlD, log crawlD.log, 18 threads, Normal priority, no affinity, venv-t126. The 30 h cap counts from this start.
# Reading rule (the coordinator, written before the run): at a 0.7 expect at most 5 Newton steps with lam 1 throughout; a step above 8 Newton steps is reported at once
# and the run goes on. Series rule (19:52 UTC): stop and report if |z_N| is above 1e-24 or a_max is below 2.0; warn once, without stopping, when a_max falls below 2.5.
# Stop rules: the three-halvings stop line, D 400, the 30 h cap, the 20 min log stall.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlC/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "9e5fd9f" ] || { echo "worktree D:/choptuik-i446 is not at 9e5fd9f" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part D start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlD --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.7 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlD.log 2>&1
rc=$?
echo "part D anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
