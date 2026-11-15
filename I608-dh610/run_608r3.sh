#!/usr/bin/env bash
# #608, third restart of d6 (the coordinator): from #836's accepted state at D 252.7855 (I836-dh370/drop/, reached with
# --od_full_drop 1e-2 where restart2_d6 refused the same attempt), with restart2's flags plus --od_full_drop 1e-2
# (#836) and the iteration-1..2 refusal --od_abort_theta 1e8 --od_abort_it 2 (#784; no accepted attempt in #603's and
# #608's logs exceeds it). 12 threads. Worktree choptuik-large-d-608r3 at main (2e315411 or later), the main checkout's
# .venv. Output restart3_d6/, log restart3_d6.log, exits in exits_608r.txt. --D_max 254 as before.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I608-dh610
B=/home/nathan/scratch608r3
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
WT=/home/nathan/Source/choptuik-large-d-608r3
S=I836-dh370/drop/anm_pin3_D252.7855.npz
mkdir -p $B/$(dirname $S)
cd $WT/hp || exit 9
git merge-base --is-ancestor 2e315411 HEAD || { echo "worktree older than 2e315411" >&2; exit 9; }
[ -s $B/$S ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S > $B/$S; } || { echo "missing $S" >&2; exit 9; }
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $B/$S \
    || { echo "unreadable $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "restart3_d6 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S, hp $(git rev-parse --short=8 HEAD)" >> $R/exits_608r.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 restart3_d6" \
  nice -n 10 $PY -u anm_run.py $B $R/restart3_d6 --state $S --kfreeze 3 --held_fit data/held_fit_d6.json --N 24 \
    --eps 1e-14 --h_max 1.0 --steps 400 --D_max 254 --threads 12 --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 \
    --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 \
    --od_full_drop 1e-2 --od_abort_theta 1e8 --od_abort_it 2 >> $R/restart3_d6.log 2>&1
rc=$?
echo "restart3_d6 anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608r.txt
exit $rc
