#!/usr/bin/env bash
# #966 ladder (proposed after leg 0's +13 polish failed): one base polish rung at ks 301 (+10) from ks_chain2's D 237.7132 state, as run903d.sh does
# its rungs (anm_run.py with the chain's flags, --steps 0 --ks K --keep_plan 0 --save_base 1, 3 h cap, gate903d.py on its log), then the dry of ks_chain3b.
# usage: bash ladder966.sh [rung|dry|chain]    (rung and chain run on the 10-thread budget, so the running ks_chain3 unit i966b must be stopped first)
WT=/home/nathan/Source/choptuik-large-d-961
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I966-dh370
T=10
PY=$WT/.venv/bin/python
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
cd $WT/hp || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
# the flags of run966.sh's F3, copied from it so that the rung and the chain see the same ones
F3=$(sed -n 's/^F3="\(.*\)"$/\1/p' $OUT/run966.sh)
[ -n "$F3" ] || { echo "no F3 in run966.sh"; exit 8; }
K=${K:-301}
case ${1:-rung} in
rung)
  out=$OUT/ladder/ks$K; mkdir -p $out
  log "ladder rung ks $K start from $BASE"
  t=$(date +%s)
  nice -n 10 timeout -s TERM 10800 $PY -u anm_run.py $RAW $out --state $BASE $F3 --steps 0 --ks $K --keep_plan 0 --save_base 1 >> $out/anm_run.log 2>&1
  rc=$?
  base=$(ls $out/base_pin*_D*.npz 2>/dev/null | head -1)
  gate=$($PY -I $OUT/gate903d.py $out/anm_run.log)
  log "ladder rung ks $K exit $rc wall $(( $(date +%s) - t ))s base ${base:-none} gate: $gate"
  case "$gate" in OK*) ;; *) log "ladder STOPPED at ks $K (gate)"; exit 1;; esac ;;
dry)
  base=$(ls $OUT/ladder/ks$K/base_pin*_D*.npz | head -1); rel=${base#$RAW/}
  $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $rel --D_stop 400 --mult 4.4 --pad -249 --dry -- $F3 --steps 400 2>&1 | grep -m1 '^leg 0:' ;;
chain)
  base=$(ls $OUT/ladder/ks$K/base_pin*_D*.npz | head -1); rel=${base#$RAW/}
  log "ks_chain3b start from $rel"
  t=$(date +%s)
  nice -n 10 $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $rel --D_stop 400 --mult 4.4 --pad -249 -- $F3 --steps 400 >> $OUT/ks_chain3b.log 2>&1
  log "ks_chain3b exit $? wall $(( $(date +%s) - t ))s" ;;
esac
