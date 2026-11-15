#!/usr/bin/env bash
# #608 restart4 (the coordinator): a chain from a state on this disk with restart3's flags, --od_abort_it 3 (the replay
# over every log refuses no accepted attempt at iteration 3, CRAWL 14) and a step cap. Used for d6 from #836's state at
# D 252.7855 with --h_max 0.25 to fill the states #808's held arm needs near D 253.53, since restart3_d6 jumped
# 252.79 -> 253.79 in one step and then stalled at that base.
# usage: run_608r4.sh d6|d10 /absolute/state.npz THREADS H_MAX D_MAX
N=${1:?d6 or d10}; STATE=${2:?state}; T=${3:-12}; H=${4:-0.25}; DM=${5:-253.6}
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
echo "restart4_$N start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $STATE, hp $(git rev-parse --short=8 HEAD), $T threads, h_max $H, D_max $DM" >> $R/exits_608r.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 restart4_$N" \
  nice -n 10 $PY -u anm_run.py / $R/restart4_$N --state $STATE --kfreeze 3 --held_fit data/held_fit_$N.json --N 24 \
    --eps 1e-14 --h_max $H --steps 400 --D_max $DM --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --jet_o 1 \
    --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 \
    --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_accept natural --od_strong 4 --reseed_start pred --save_jet 1 \
    --od_full_drop 1e-2 --od_abort_theta 1e8 --od_abort_it 3 >> $R/restart4_$N.log 2>&1
rc=$?
echo "restart4_$N anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608r.txt
exit $rc
