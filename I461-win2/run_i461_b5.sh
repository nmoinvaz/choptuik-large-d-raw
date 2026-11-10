#!/usr/bin/env bash
# #461 part B5: crawlB4 continued from its last saved state, with a fresh log. B4 was killed at 17:14:41 UTC because its log file had been replaced under the
# running process by a git autostash of mine (crawlB4.log stopped growing at 17:12:27 UTC, the run, the states and anm_run.jsonl were fine).
# Same command as B4 (--qd_it 40 --od_junk 0 --h_max 1.0 --steps 400 --D_max 400, d84cc51, 18 threads, no --base_adopt), output crawlB5, log crawlB5.log.
# Stop rules: the three-halvings stop line, D 400, the 30 h cap from B4's start (21:51:31 UTC on 2026-11-11, the coordinator's order of 15:49 UTC),
# the 20 min log stall (watched by a separate loop), and the coordinator's series rule: every base's series line must keep |z_N| below 1e-27 and
# a_max above 3, else stop and report.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlB4/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "d84cc51" ] || { echo "worktree D:/choptuik-i446 is not at d84cc51" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part B5 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlB5 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawlB5.log 2>&1
rc=$?
echo "part B5 anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
