#!/usr/bin/env bash
# #608, the coordinator's restart (message of 2026-11-13): one comparison chain from its newest converged state, on a worktree of
# main at a515ab87, with #603's corrector flags (--a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4
# --reseed_start pred --qd_it 20 --save_jet 1) and everything else as run_608.sh. Output in restart_<chain>/.
# usage: run_608r.sh d6|d10 STATE   (STATE relative to the raw clone)
N=${1:?d6 or d10}
STATE=${2:?state}
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I608-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
WT=/home/nathan/Source/choptuik-i608b
cd $WT/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "a515ab87" ] || { echo "worktree is not at a515ab87" >&2; exit 9; }
[ -f $RAW/$STATE ] || { echo "missing $STATE" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "restart_$N start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $STATE" >> $R/exits_608r.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 restart_$N" \
  $PY -u anm_run.py $RAW $R/restart_$N --state $STATE --kfreeze 3 --held_fit data/held_fit_$N.json --N 24 --eps 1e-14 \
    --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 --reseed 2 \
    --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 \
    >> $R/restart_$N.log 2>&1
rc=$?
echo "restart_$N anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608r.txt
exit $rc
