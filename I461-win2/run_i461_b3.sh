#!/usr/bin/env bash
# #461 part B3: the chain from D 215.13125 to D 400 at d84cc51 (branch fix/base-polish-not-adopted), started by the coordinator's order of
# 2026-11-10 14:12 UTC after part B2's step 1 stalled near 1e-31 with "1 junk directions frozen" (B2 was stopped at 14:13:39 UTC).
# Part B's command with --od_junk 0 --h_max 1.0 --steps 400 --D_max 400, from B2's accepted state crawlB2/anm_pin3_D215.1312.npz,
# output crawlB3, log crawlB3.log, 18 threads, no --base_adopt, Normal priority, no affinity, venv-t126.
# Stop rules: the three-halvings stop line (a 1.0, 0.5, 0.25, 0.125), D 400, a 24 h cap from the start (watched by a separate loop),
# the 20 min log stall (the same).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/crawlB2/anm_pin3_D215.1312.npz
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "d84cc51" ] || { echo "worktree D:/choptuik-i446 is not at d84cc51" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part B3 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlB3 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawlB3.log 2>&1
rc=$?
echo "part B3 anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
