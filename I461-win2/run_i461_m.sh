#!/usr/bin/env bash
# #461 crawlM: the chain from crawlL's last saved state (crawlL/anm_pin3_D242.5225.npz, D 242.522462463) at main e5bbdcd (the re-seed rung fix), crawlL's command (--a0 0.0078125 --h_max 0.0625; a_grow 1.25,
# a_hold 1, lam_stall 0.04, qd_it 12, tol_od 1e-60, the base polish on), the coordinator's order of 2026-11-11 17:50 UTC. Python only: interpreter and hpkernel build of venv-t126; worktree D:/choptuik-i446e at e5bbdcd.
# Output crawlM, log crawlM.log, 18 threads, 24 h cap. Stop rule (guard_m.sh): an attempt refused at a 0.0078125 or below.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/crawlL/anm_pin3_D242.5225.npz
cd /d/choptuik-i446e/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "e5bbdcd" ] || { echo "worktree D:/choptuik-i446e is not at e5bbdcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part M start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at e5bbdcd from $S a0 0.0078125 h_max 0.0625" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlM --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --a0 0.0078125 --h_max 0.0625 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/crawlM.log 2>&1
rc=$?
echo "part M anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
