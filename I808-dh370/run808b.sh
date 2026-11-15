#!/bin/bash
# #808 on dh370 (the coordinator): the plan arm again with the full-step drop (#808's recommended task 2). The plan
# arm's polishes did not converge (06:24 UTC): at the middle states step 1's lam 1 trial fell to 3e-36..7e-31 and the
# own test refused it. --od_full_drop 1e-6 accepts a full step whose max|F| falls to 1e-6 of the start's (#709, #777).
# Each job polishes one #603 state at its own D (--steps 0, #603's flags, --save_base 1), #603's own held values
# (data/held_fit.json), the base planned again (--keep_plan 0), plus the drop. The same five states. table808.py
# reads this arm with --plan_tag=plandrop, by the rule registered on #808.
#   bash run808b.sh plandrop   five jobs, 3 at a time at 4 threads each, then table808.py --plan_tag=plandrop
# Worktree choptuik-large-d-808b at main (38744bb3 or later) with venv-i800. The inputs are the first run's, in B.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I808-dh370
B=/home/nathan/scratch808
WT=/home/nathan/Source/choptuik-large-d-808b
PY=/home/nathan/Source/venv-i800/bin/python
STATES="240.1244 250.8381 251.8859 252.6135 253.5301"
mkdir -p $B $R
log() { echo "808 $1 $(date -u '+%F %T') UTC" >> $R/exits_808.txt; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 38744bb3 HEAD || { log "worktree $WT is older than 38744bb3"; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_base 1"
job() {  # D arm threads
  local D=$1 arm=$2 T=$3 tag=s$1_$2 extra
  case $arm in
    d6) extra="--held_fit data/held_fit_d6.json --held_from $B/I608-dh610/chain_d6/anm_pin3_D243.1312.npz" ;;
    d10) extra="--held_fit data/held_fit_d10.json --held_from $B/I608-dh610/chain_d10/anm_pin3_D242.1312.npz" ;;
    plan) extra="--held_fit data/held_fit.json --keep_plan 0" ;;
    plandrop) extra="--held_fit data/held_fit.json --keep_plan 0 --od_full_drop 1e-6" ;;
    *) log "unknown arm $arm"; return 9 ;;
  esac
  mkdir -p $R/$tag
  log "$tag start, $T threads"
  nice -n 10 $PY -u anm_run.py $RAW $R/$tag --state $B/I603-win2/chain/anm_pin3_D$D.npz $FLAGS --threads $T $extra > $R/$tag.log 2>&1
  log "$tag exit $?"
}
case $1 in
  job) shift; job "$@"; exit $? ;;
  plandrop) ;;
  *) echo "usage: run808b.sh plandrop"; exit 2 ;;
esac
log "plandrop start, hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)'), hp $(git rev-parse --short=8 HEAD)"
for D in $STATES; do echo "$D plandrop 4"; done | xargs -P 3 -L 1 bash $0 job
$PY -I $R/table808.py $R --plan_tag=plandrop > $R/table808_plandrop.txt 2>&1; log "table plandrop exit $?"
log "plandrop done"
