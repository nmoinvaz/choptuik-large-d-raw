#!/usr/bin/env bash
# #608: one comparison chain (held fit of degree 6 or 10) on main's exact freeze projector, from its D 225.13 state,
# #462's d6_long3.cmd / d10_long3.cmd flags, the base polish on, --threads 9, --save_base 1 (the control's input).
# usage: run_608.sh d6|d10 [STATE relative to the raw clone; a restart names the chain's last saved state]
N=${1:?d6 or d10}
RAW=/home/nathan/Source/choptuik-large-d-raw
STATE=${2:-I462-win/chain_$N/anm_pin3_D225.1312.npz}
R=$RAW/I608-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
WT=/home/nathan/Source/choptuik-i608
cd $WT/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "a879ccc3" ] || { echo "worktree is not at a879ccc3" >&2; exit 9; }
[ -f $RAW/$STATE ] || { echo "missing $STATE" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "chain_$N start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $STATE" >> $R/exits_608.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#608 chain_$N" \
  $PY -u anm_run.py $RAW $R/chain_$N --state $STATE --kfreeze 3 --held_fit data/held_fit_$N.json --N 24 --eps 1e-14 \
    --h_max 1.0 --steps 400 --D_max 400 --threads 9 --corrector od --tol_od 1e-60 --qd_it 12 --jet_o 1 --reseed 2 \
    --reseed_q 1 --save_pred 1 --od_junk 0 --held_o 1 --reseed_o 3 --save_base 1 >> $R/chain_$N.log 2>&1
rc=$?
echo "chain_$N anm_run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_608.txt
exit $rc
