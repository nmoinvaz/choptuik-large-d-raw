#!/usr/bin/env bash
# #461 crawlH: crawlG restarted from its last saved state (D 232.63125, which carries its plan), at main cc6d51b, crawlG's command with --h_max 0.5 and --qd_it 8, --steps 400,
# output crawlH, log crawlH.log, 18 threads, Normal priority, no affinity, venv-t126, by the coordinator's order of 2026-11-11 00:24 UTC (crawlG stopped 00:25:20 UTC: its a 1.0
# attempt from D 232.63125 stalled at lam 0.03). The 30 h cap counts from this start. The log must print "the base keeps its stored plan" and the first step must be clean.
# Reading rule: 3 Newton steps at a 0.5 with lam 1. Report at once a refusal with its lines, any lam below 1, and the series line if |z_N| goes above 1e-27 or the fourth ratio
# below 100. Hourly table as crawlG's, with the Delta comparison against the first chain where the D coincide. A cap of 8 Newton steps ends a stalled attempt after about 12 min.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlG/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "cc6d51b" ] || { echo "worktree D:/choptuik-i446 is not at cc6d51b" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part H start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlH --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.5 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 8 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlH.log 2>&1
rc=$?
echo "part H anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
