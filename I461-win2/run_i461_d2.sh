#!/usr/bin/env bash
# #461 crawlD2: crawlD again from the same state (crawlD's last saved state), at main cc6d51b, with --od_junk 0 and --h_max 0.35 (--steps 400, output crawlD2, log crawlD2.log),
# started when pilot E's first od: line read "0 junk directions frozen" (the coordinator's reading rule of 2026-11-10 20:38 UTC). 18 threads, Normal priority, no affinity, venv-t126.
# Rules as crawlD: at most 5 Newton steps expected after the first (restart) step, series rule (stop above |z_N| 1e-24 or under a_max 2.0, warn under a_max 2.5), the 30 h cap from this start.
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
echo "part D2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlD2 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.35 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --base_polish 0 --save_pred 1 > $R/crawlD2.log 2>&1
rc=$?
echo "part D2 anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
