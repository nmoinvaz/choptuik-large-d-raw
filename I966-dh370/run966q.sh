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
WT=/home/nathan/Source/choptuik-large-d-966g     # code: perf/elim-projections 1aa4a4fb (#1032 round 2, with eb1002cf); python and hpkernel (40f4b4a5 build, no residual_sub) from -961
VENV=/home/nathan/Source/choptuik-large-d-961    # python and the built hpkernel
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I966-dh370
T=10
PY=$VENV/.venv/bin/python
export VIRTUAL_ENV=$VENV/.venv PATH=$VENV/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
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
  chainc)      # restart of ks_chain3b with --reseed_qd_bar 1e-15 (coordinator's hc 2026-11-19), --pad -273 keeps the resumed leg at the state's ks 291
    stage ks_chain3c $OUT/ks_chain3b_c.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad -273 -- $F3 --reseed_qd_bar 1e-15 --steps 400 || exit 1 ;;
  chainc0)     # the same with the literal --pad -262 (resumed leg at ks 302)
    stage ks_chain3c0 $OUT/ks_chain3b_c.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad -262 -- $F3 --reseed_qd_bar 1e-15 --steps 400 || exit 1 ;;
  chaind)      # restart 2026-11-19 ~03:10 UTC (coordinator's hc): --reseed_qd_bar 1e-13, --pad -281 keeps the resumed leg at the state's ks 293 (no order jump)
    stage ks_chain3d $OUT/ks_chain3b_d.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad -281 -- $F3 --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chaine)      # restart 2026-11-19 (coordinator's hc): a rule level held at 0.00715 (--a_scale 0.00715 --a_rise 1), --reseed_qd_bar 1e-13, PAD from the environment keeps the resumed leg at ks 293
    [ -n "$PAD" ] || { log "chaine: PAD not set"; exit 9; }
    F3e="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    stage ks_chain3e $OUT/ks_chain3b_e.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3e --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chainf)      # restart 2026-11-19 (coordinator's hc): the tolerance set to the projection's floor, --tol_od 1e-34 (for 1e-60), a rule level held at 0.00715, bar 1e-13, PAD from the environment
    [ -n "$PAD" ] || { log "chainf: PAD not set"; exit 9; }
    F3f="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3f="${F3f/--tol_od 1e-60/--tol_od 1e-34}"
    stage ks_chain3f $OUT/ks_chain3b_f.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3f --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chaing)      # restart 2026-11-19 (coordinator's hc): --tol_od 1.5e-35 (the bar's: |F|/sigma_Delta <= 1e-18), level held at 0.00715, bar 1e-13, from D 250.7060 (the D 251.2845 state, 3.5e-35, is renamed bar_failed_*), PAD from the environment
    [ -n "$PAD" ] || { log "chaing: PAD not set"; exit 9; }
    F3g="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3g="${F3g/--tol_od 1e-60/--tol_od 1.5e-35}"
    stage ks_chain3g $OUT/ks_chain3b_g.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3g --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chainh)      # restart 2026-11-19 (coordinator's hc): --tol_od 2e-34 (step 2 under 1.5e-35 crawled at 4e-35..1.2e-34), level held at 0.00715, bar 1e-13, from the leg 5 state at D 251.2845, PAD from the environment
    [ -n "$PAD" ] || { log "chainh: PAD not set"; exit 9; }
    F3h="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3h="${F3h/--tol_od 1e-60/--tol_od 2e-34}"
    stage ks_chain3h $OUT/ks_chain3b_h.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3h --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chaini)      # floor rule (coordinator's hc 2026-11-19): --tol_od 2e-34 --od_floor_delta 1e-30, code from -966f, else as chainh; PAD from the environment
    [ -n "$PAD" ] || { log "chaini: PAD not set"; exit 9; }
    F3i="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3i="${F3i/--tol_od 1e-60/--tol_od 2e-34} --od_floor_delta 1e-30"
    stage ks_chain3i $OUT/ks_chain3b_i.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3i --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chainj)      # leg 7 on (coordinator's hc 2026-11-19/20, #1032 round 2): chainh's flags plus --proj_start pred --reseed_o_stop 1 (no --proj_o), code from -966g (1aa4a4fb); PAD from the environment
    [ -n "$PAD" ] || { log "chainj: PAD not set"; exit 9; }
    F3j="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3j="${F3j/--tol_od 1e-60/--tol_od 2e-34} --proj_start pred --reseed_o_stop 1"
    stage ks_chain3j $OUT/ks_chain3b_j.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3j --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chaink)      # leg 7 on (coordinator's hc 2026-11-20, #1032 round 2 + floor rule): chainh's flags plus --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 (no --proj_o), code from -966g (1aa4a4fb); PAD from the environment
    [ -n "$PAD" ] || { log "chaink: PAD not set"; exit 9; }
    F3k="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3k="${F3k/--tol_od 1e-60/--tol_od 2e-34} --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30"
    stage ks_chain3k $OUT/ks_chain3b_k.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3k --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chainm)      # coordinator's rule 2026-11-20 (leg 7 step 0 slow or several corrections): chaink's flags plus --proj_o 1 (bar = --tol_od), code from -966g (1aa4a4fb); PAD from the environment
    [ -n "$PAD" ] || { log "chainm: PAD not set"; exit 9; }
    F3m="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3m="${F3m/--tol_od 1e-60/--tol_od 2e-34} --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1"
    stage ks_chain3m $OUT/ks_chain3b_m.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3m --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  chainq)      # coordinator's A/B (hc 2026-11-20, NOT STARTED before his confirmation): chainm's flags with --od_accept own (hp's own trial test, the default) for natural; same state, same code (1aa4a4fb), PAD from the environment
    [ -n "$PAD" ] || { log "chainq: PAD not set"; exit 9; }
    F3q="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
    F3q="${F3q/--tol_od 1e-60/--tol_od 2e-34} --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1"
    [[ "$F3q" == *"--od_accept natural"* ]] || { log "chainq: F3 has no --od_accept natural to replace"; exit 9; }
    F3q="${F3q/--od_accept natural/--od_accept own}"
    stage ks_chain3q $OUT/ks_chain3b_q.log $PY -u ks_chain.py $RAW $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD -- $F3q --reseed_qd_bar 1e-13 --steps 400 || exit 1 ;;
  *) log "unknown stage $s"; exit 3 ;;
  esac
done
log "stages $* done"
