#!/usr/bin/env bash
# #608, third restart of a chain from a state on this disk (the coordinator): restart2's flags plus --od_full_drop 1e-2
# (#836) and --od_abort_theta 1e8 --od_abort_it 2 (#784). d10's refused attempts at D 252.9464 (lam 1 trials lowering
# max|F| 3e7, 5e6 and 340 times, refused on the correction ratio) are what the drop accepts.
# usage: run_608r3b.sh d6|d10 /absolute/path/state.npz THREADS
N=${1:?d6 or d10}
STATE=${2:?absolute state path}
T=${3:-8}
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I608-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
WT=/home/nathan/Source/choptuik-large-d-608r3
cd $WT/hp || exit 9
git merge-base --is-ancestor 2e315411 HEAD || { echo "worktree older than 2e315411" >&2; exit 9; }
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $STATE \
    || { echo "unreadable $STATE" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "restart3_$N start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $STATE, hp $(git rev-parse --short=8 HEAD), $T threads" >> $R/exits_608r.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 restart3_$N" \
  nice -n 10 $PY -u anm_run.py / $R/restart3_$N --state $STATE --kfreeze 3 --held_fit data/held_fit_$N.json --N 24 \
    --eps 1e-14 --h_max 1.0 --steps 400 --D_max 254 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 \
    --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 \
    --od_full_drop 1e-2 --od_abort_theta 1e8 --od_abort_it 2 >> $R/restart3_$N.log 2>&1
rc=$?
echo "restart3_$N anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608r.txt
exit $rc
