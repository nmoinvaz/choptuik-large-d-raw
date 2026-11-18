#!/usr/bin/env bash
# #966 on dh370: #961's two recommended checks, then ks_chain3, on the build of 40f4b4a5 (worktree -961, its .venv), T = 10 threads at
# nice 10, from hp/. usage: bash run966.sh STAGE...    stages: test doff dry chain
#   test   cargo test --release --lib oseries_ -- --nocapture --test-threads=1 with RUSTFLAGS="-C target-cpu=native"
#   doff   #961's step (d) with --jet_tangent_from 0 --series_split 0, all else as in #961 (flags of run961.sh)
#   dry    ks_chain.py --dry with #966's flags
#   chain  ks_chain.py with #966's flags (no timeout, no kill rule; the stops are the driver's own)
#   dryb chainb  ks_chain3b (coordinator's hc, 2026-11-18 ~21:10 UTC): the same from the same state with --pad -262 (leg 0 at the state's ks 291) and F3b = F3 plus
#          --reseed_qd_bar 1e-21, on main 664ef3dd (-961 fast-forwarded, build kept), OUT I966-dh370/ks_chain3b
# The watcher only logs and alerts (mem966.log, alerts966.txt, an hc message at most every 10 min); it never stops or kills anything.
WT=/home/nathan/Source/choptuik-large-d-961
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I966-dh370
T=10
PY=$WT/.venv/bin/python
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
cd $WT/hp || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }

watch() {
  last=0
  while sleep 30; do
    now=$(date +%s)
    read -r used avail swap < <(free -m | awk '/^Mem:/{u=$3;a=$7} /^Swap:/{s=$3} END{print u,a,s}')
    procs=$(ps -eo rss=,pcpu=,comm=,args= | awk '($3 ~ /^python/ && /(anm_run|ks_chain)\.py/) || $3 ~ /^(rustc|hpkernel)/ {printf "%s %d MB %s%% ", $3, $1/1024, $2}')
    echo "$(date -u '+%F %T') used ${used} avail ${avail} swap ${swap} load $(cut -d' ' -f1 /proc/loadavg) | ${procs}" >> $OUT/mem966.log
    if [ "$swap" -gt 6500 ] || [ "$avail" -lt 500 ]; then
      echo "$(date -u '+%F %T') ALERT swap ${swap} avail ${avail}" >> $OUT/alerts966.txt
      if [ $((now - last)) -ge 600 ]; then
        last=$now
        hc send nathans-macbook-air-m5-3/t5 "dh370 #966 memory alert: swap ${swap} MB, available ${avail} MB (watcher only logs, nothing stopped)" >/dev/null 2>&1
      fi
    fi
  done
}

stage() {                         # stage NAME LOG CMD...
  name=$1; lg=$2; shift 2
  echo "== $name $(date -u '+%F %T') $(git -C $WT rev-parse --short HEAD) $*" > $lg
  log "$name start"
  t=$(date +%s)
  nice -n 10 "$@" >> $lg 2>&1
  rc=$?
  echo "exit $rc" >> $lg
  log "$name exit $rc wall $(( $(date +%s) - t ))s"
  if grep -q '^Traceback' $lg; then log "$name Traceback in $(basename $lg), stop"; return 99; fi
  return 0
}

watch & WP=$!
trap 'kill $WP 2>/dev/null' EXIT

# #961's (d), run961.sh's flags, the same state
ST961=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --keep_plan 0 --D_max 240 --steps 1"
# ks_chain3: #961 (d)'s flags with --qd_it 40 for 20, 400 steps
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
F3="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.0715 --jet_tangent_from 1 --series_split 1"

F3b="$F3 --reseed_qd_bar 1e-21"

for s in "$@"; do
  case $s in
  test)
    export RUSTFLAGS="-C target-cpu=native" CARGO_BUILD_JOBS=6 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
    stage cargo_test_native $OUT/cargo_test_native.log cargo test --release --lib oseries_ -- --nocapture --test-threads=1 || exit 1
    unset RUSTFLAGS ;;
  doff)
    stage step_n31_off $OUT/step_n31_off.log timeout -s TERM 7200 $PY -u anm_run.py $RAW $OUT/step_n31_off --state $ST961 $CH \
      --N 31 --ks 240 --jet_tangent_from 0 --series_split 0 --a_rule reseed --a_scale 0.0715 || exit 1 ;;
  dry)
    stage ks_chain3_dry $OUT/ks_chain3_dry.log $PY -u ks_chain.py $RAW $OUT/ks_chain3 --state $BASE --D_stop 400 --mult 4.4 --pad -249 --dry -- $F3 --steps 400 || exit 1 ;;
  chain)
    stage ks_chain3 $OUT/ks_chain3.log $PY -u ks_chain.py $RAW $OUT/ks_chain3 --state $BASE --D_stop 400 --mult 4.4 --pad -249 -- $F3 --steps 400 || exit 1 ;;
  dryb)
    stage ks_chain3b_dry $OUT/ks_chain3b_dry.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad -262 --dry -- $F3b --steps 400 || exit 1 ;;
  chainb)
    stage ks_chain3b $OUT/ks_chain3b.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad -262 -- $F3b --steps 400 || exit 1 ;;
  *) log "unknown stage $s"; exit 3 ;;
  esac
done
log "stages $* done"
