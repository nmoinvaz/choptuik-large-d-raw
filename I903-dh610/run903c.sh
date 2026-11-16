#!/bin/bash
# #903 on dh610 (the coordinator's order of 2026-11-16 16:11 UTC, my launcher): order 160 from D 200. Worktree
# choptuik-large-d-903 at main 423bd22d (the series one order at a time), hpkernel from #911's build, chain_nsr's flags,
# 10 threads, nice 10. 1. p130_200: the control at the state's own order, --steps 0 --D_max 201 --save_base 1. 2. p160_200:
# the same with --ks 160 --keep_plan 0; if it fails, rungs 140, 150, 160 each from the previous rung's saved base, a failed
# +10 rung retried as two +5 rungs, and the ladder stops at a failed +5 rung. 3. chain_k160 from the 160 base, --ks 160
# --keep_plan 1 --steps 400 --D_max 262. A rung is ok when anm_run exits 0, its octo-double polish converged with
# max|F| <= 1e-60 and its base is saved. Each rung's end is a line "903 rung ..." in exits_903.txt.
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-903
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I903-dh610
B=/home/nathan/scratch903
PY=/home/nathan/Source/choptuik-large-d-911/.venv/bin/python
S0=T138-win2/chain_o/anm_pin3_D200.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
log() { echo "903 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_903.txt; }
mkdir -p $B/$(dirname $S0) $OUT
ln -sfn $OUT $B/I903-dh610
[ -s $B/$S0 ] || { git -C $RAW fetch -q origin && git -C $RAW show origin/main:$S0 > $B/$S0; } || { log "missing $S0"; exit 9; }
$PY -I -c "import sys, numpy as np; z = np.load(sys.argv[1], allow_pickle=False); [z[k] for k in z.files]" $B/$S0 || { log "unreadable $S0"; exit 9; }
cd $WT/hp || exit 9
git merge-base --is-ancestor 423bd22d HEAD || { log "worktree older than 423bd22d"; exit 9; }
log "start order-160 run, hp $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
BASE=""   # the saved base of the last ok rung, relative to $B
# rung NAME STATE KS: a polish with --steps 0; sets BASE to the saved base and returns 0 when the rung is ok
rung() {
  local name=$1 state=$2 ks=$3 extra="" t=$(date +%s)
  [ -n "$ks" ] && extra="--ks $ks --keep_plan 0"
  PYTHONFAULTHANDLER=1 nice -n 10 $PY -u anm_run.py $B $OUT/$name --state $state $F $extra --steps 0 --D_max 201 --save_base 1 \
    >> $OUT/$name.log 2>&1
  local rc=$? base fmax
  base=$(ls $OUT/$name/base_pin3_*.npz 2>/dev/null | head -1)
  fmax=$(grep -o 'octo-double Newton: [0-9]* steps, max|F| [^,]*, converged' $OUT/$name.log | tail -1 | sed 's/.*max|F| //; s/,.*//')
  local ok=no
  if [ $rc -eq 0 ] && [ -n "$base" ] && [ -n "$fmax" ] && $PY -c "import sys; sys.exit(0 if float(sys.argv[1]) <= 1e-60 else 1)" $fmax; then ok=yes; fi
  log "rung $name ks ${ks:-state} exit $rc wall $(( $(date +%s) - t )) s max|F| ${fmax:-none} base ${base:+saved} ok $ok"
  [ $ok = yes ] || return 1
  BASE=I903-dh610/$name/$(basename $base)
}
rung p130_200 $S0 "" || { log "control p130_200 failed, stop"; exit 1; }
B130=$BASE
if rung p160_200 $S0 160; then
  B160=$BASE
else
  log "p160_200 failed, the ladder 140, 150, 160"
  cur=$B130; k=130
  for t in 140 150 160; do
    if rung p${t}_200 $cur $t; then cur=$BASE; k=$t; continue; fi
    mid=$(( (k + t) / 2 ))
    rung p${mid}_200 $cur $mid || { log "ladder stops at the failed +5 rung $mid"; exit 1; }
    cur=$BASE; k=$mid
    rung p${t}_200b $cur $t || { log "ladder stops at the failed +5 rung $t"; exit 1; }
    cur=$BASE; k=$t
  done
  B160=$cur
fi
log "chain_k160 starts from $B160"
t=$(date +%s)
PYTHONFAULTHANDLER=1 nice -n 10 $PY -u anm_run.py $B $OUT/chain_k160 --state $B160 $F --ks 160 --keep_plan 1 --steps 400 --D_max 262 \
  >> $OUT/chain_k160.log 2>&1
rc=$?
log "anm_run chain_k160 exit $rc wall $(( $(date +%s) - t )) s"
exit $rc
