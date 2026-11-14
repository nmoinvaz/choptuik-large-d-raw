#!/usr/bin/env bash
# #608, second restart, after dh610's reboot of 2026-11-13 22:52 UTC killed both restart chains. One comparison chain from
# its newest converged state, as run_608r.sh (worktree, build and corrector flags unchanged), with three changes. It uses 8
# threads, since another project holds 4 of the 20. Output goes to restart2_<chain>/. --D_max 254 ends the chain at the
# coordinator's stop past D 253.7.
# usage: run_608r2.sh d6|d10 STATE   (STATE relative to the raw clone)
N=${1:?d6 or d10}
STATE=${2:?state}
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I608-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
WT=/home/nathan/Source/choptuik-i608b
cd $WT/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "a515ab87" ] || { echo "worktree is not at a515ab87" >&2; exit 9; }
[ -f $RAW/$STATE ] || { echo "missing $STATE" >&2; exit 9; }
# Every array is read, so a state the reboot truncated fails here (zip CRC) and not inside the run.
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $RAW/$STATE \
    || { echo "unreadable $STATE" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "restart2_$N start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $STATE" >> $R/exits_608r.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 restart2_$N" \
  nice -n 10 $PY -u anm_run.py $RAW $R/restart2_$N --state $STATE --kfreeze 3 --held_fit data/held_fit_$N.json --N 24 \
    --eps 1e-14 --h_max 1.0 --steps 400 --D_max 254 --threads 8 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 \
    --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 \
    >> $R/restart2_$N.log 2>&1
rc=$?
echo "restart2_$N anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608r.txt
exit $rc
