#!/bin/bash
# #808 on dh370 (the coordinator): Delta at fixed D under other held values and under another plan, at #603's states.
# Each job polishes one #603 state at its own D (anm_run --steps 0, #603's flags, --save_base 1) with one change:
#   d6, d10  the held values of #608's chain of that fit, carried to D by the fit (--held_from, 0209d4d2), #603's plan
#   plan     #603's own held values (data/held_fit.json), the base planned again (--keep_plan 0)
# States D 240.1244 (the control) and 250.8381, 251.8859, 252.6135, 253.5301. Rule and controls: table808.py.
#   bash run808.sh pilot   253.5301 d10 (the hardest: the largest held shift, the smallest p_min) and the control
#                          240.1244 d6, 6 threads each, then table808.py --pilot
#   bash run808.sh rest    the other 13 jobs, 3 at a time at 4 threads each, then table808.py
# Worktree choptuik-large-d-808 at main 0209d4d2 with venv-i800 (main's kernel at ccc520e1 plus ks_w_from, off).
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I808-dh370
B=/home/nathan/scratch808
WT=/home/nathan/Source/choptuik-large-d-808
PY=/home/nathan/Source/venv-i800/bin/python
STATES="240.1244 250.8381 251.8859 252.6135 253.5301"
mkdir -p $B $R
log() { echo "808 $1 $(date -u '+%F %T') UTC" >> $R/exits_808.txt; }
cd $WT/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "0209d4d2" ] || { log "worktree $WT is not at 0209d4d2"; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_base 1"
job() {  # D arm threads
  local D=$1 arm=$2 T=$3 tag=s$1_$2 extra
  case $arm in
    d6) extra="--held_fit data/held_fit_d6.json --held_from $B/I608-dh610/chain_d6/anm_pin3_D243.1312.npz" ;;
    d10) extra="--held_fit data/held_fit_d10.json --held_from $B/I608-dh610/chain_d10/anm_pin3_D242.1312.npz" ;;
    plan) extra="--held_fit data/held_fit.json --keep_plan 0" ;;
    *) log "unknown arm $arm"; return 9 ;;
  esac
  mkdir -p $R/$tag
  log "$tag start, $T threads"
  nice -n 10 $PY -u anm_run.py $RAW $R/$tag --state $B/I603-win2/chain/anm_pin3_D$D.npz $FLAGS --threads $T $extra > $R/$tag.log 2>&1
  log "$tag exit $?"
}
case $1 in
  job) shift; job "$@"; exit $? ;;
  pilot|rest) ;;
  *) echo "usage: run808.sh pilot|rest"; exit 2 ;;
esac
# inputs: #603's states and #608's last states, read from the raw repository's GitHub copy (the live clone is not pulled)
git -C $RAW fetch -q origin || { log "fetch failed"; exit 9; }
for f in $(for D in $STATES; do echo I603-win2/chain/anm_pin3_D$D.npz; done) I608-dh610/chain_d6/anm_pin3_D243.1312.npz I608-dh610/chain_d10/anm_pin3_D242.1312.npz; do
  [ -s $B/$f ] || { mkdir -p $B/$(dirname $f); git -C $RAW show origin/main:$f > $B/$f || { log "missing $f"; exit 9; }; }
done
log "$1 start, inputs in $B, hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)')"
if [ "$1" = pilot ]; then
  job 253.5301 d10 6 &
  job 240.1244 d6 6 &
  wait
  $PY -I $R/table808.py $R --pilot > $R/table808_pilot.txt 2>&1; log "table --pilot exit $?"
else
  for D in $STATES; do for arm in d6 d10 plan; do
    case "$D $arm" in "253.5301 d10"|"240.1244 d6") continue ;; esac
    echo "$D $arm 4"
  done; done | xargs -P 3 -L 1 bash $0 job
  $PY -I $R/table808.py $R > $R/table808.txt 2>&1; log "table exit $?"
fi
log "$1 done"
