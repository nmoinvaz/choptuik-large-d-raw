#!/bin/bash
# #800 stage 1 on dh370 (notes/FACTORED_HORIZON.md 4.7): the homotopy in the horizon series' tail at D 245.1366, orders
# 131..250 weighted by w (--ks 250 --ks_w W --ks_w_from 131), each rung from the last's base, from #696's r130k base
# (re-planned at ks 130, converged). 12 threads, nice 10, worktree choptuik-large-d-800 at wip/i800 with venv-i800 (its
# own release build). Then near_null.py's sigma_1..4 at w = 0, 1/2 and 1, and table800.py.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I800-dh370
B=/home/nathan/scratch800
WT=/home/nathan/Source/choptuik-large-d-800
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I696-win2/D245/r130k/base_pin3_D245.1366.npz > $B/r130k_base.npz
cd $WT/hp && . /home/nathan/Source/venv-i800/bin/activate
python -c "import sys; from hpkernel._hpkernel import Solver; sys.exit(0 if hasattr(Solver, 'set_ks_w_from') else 1)" || { echo "venv-i800's hpkernel has no set_ks_w_from: build it first" > $R/exits_800.txt; exit 9; }
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 12 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --log_proj 1"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), branch $(git rev-parse --short=8 HEAD)" > $R/exits_800.txt
log() { echo "800 $1 $(date -u '+%F %T') UTC" >> $R/exits_800.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
base_of() { ls $R/$1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
run() {  # tag state w qd_it extra...
  local tag=$1 st=$2 w=$3 qi=$4; shift 4
  mkdir -p $R/$tag
  log "$tag start, state $st, ks_w $w $*"
  nice -n 10 python -u anm_run.py $RAW $R/$tag --state $st $FLAGS --qd_it $qi --ks 250 --ks_w $w --ks_w_from 131 "$@" > $R/$tag.log 2>&1
  log "$tag exit $? converged: $(converged $R/$tag.log && echo yes || echo NO)"
}
run t0 $B/r130k_base.npz 0 20 --keep_plan 0
prev=t0
for w in 0.015625 0.03125 0.0625 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1; do
  tag=t${w#0.}; [ "$w" = 1 ] && tag=t1
  b=$(base_of $prev); [ -n "$b" ] || { log "$tag: no base from $prev, the climb stops"; break; }
  run $tag $b $w 30
  converged $R/$tag.log || { log "$tag did not converge, the climb stops"; break; }
  prev=$tag
done
for tag in t0 t5 t1; do
  b=$(base_of $tag); [ -n "$b" ] || continue
  nice -n 10 python -u near_null.py $RAW $b --k=4 --its=16 --threads=12 --json=$R/sigma_$tag.json > $R/sigma_$tag.log 2>&1
  log "sigma $tag exit $?"
done
python -I $R/table800.py $R > $R/table800.txt 2>&1; log "table exit $?"
log "all done"
