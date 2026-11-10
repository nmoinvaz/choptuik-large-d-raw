#!/usr/bin/env bash
# #461 part B4: crawlB3 continued with --qd_it 40, by the coordinator's order of 2026-11-10 15:49 UTC (B3 was stopped at 15:51:07 UTC because the
# Newton count per step rose 4, 5, 7, 10 and the cap of 12 would refuse the next steps for no better reason). From B3's last saved state,
# at d84cc51 (branch fix/base-polish-not-adopted), part B3's command with --qd_it 40 (--od_junk 0 --h_max 1.0 --steps 400 --D_max 400), output crawlB4,
# log crawlB4.log, 18 threads, no --base_adopt, Normal priority, no affinity, venv-t126.
# Stop rules: the three-halvings stop line, D 400, a 30 h cap from this start, the 20 min log stall (watched by a separate loop), and the coordinator's
# series rule: every base's series line must keep |z_N| below 1e-27 and a_max above 3, else stop and report.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlB3/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "d84cc51" ] || { echo "worktree D:/choptuik-i446 is not at d84cc51" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part B4 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlB4 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --qd_it 40 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --save_pred 1 > $R/crawlB4.log 2>&1
rc=$?
echo "part B4 anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
