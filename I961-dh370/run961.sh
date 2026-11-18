#!/usr/bin/env bash
# #961 on dh370: the issue's lines as written, on the build of perf/series-par-at 40f4b4a5 (worktree -961, its .venv), T = 10 threads at
# nice 10, from hp/. usage: bash run961.sh STAGE...    stages: test jbo tf split a b c d delta
#   test   line 1, cargo test --release --lib oseries_ (with --nocapture --test-threads=1, as in #957)
#   jbo    line 2, the 10-thread save and the 4-thread compare
#   tf     line 3, --tangent_from 1 at ST and ST2, 3 at ST
#   split  line 4
#   a b c d  line 5's chain steps, each capped at 2 h (timeout), logs step_off step_on step_ks250 step_n31
#   delta  line 5's Delta test: (b) against (a) at most 1e-40, (c) against (a) above 1e-40
# A Traceback in a stage's log stops the list; a non-zero exit alone does not (a failed check is a result). The watcher only logs
# and alerts (mem961.log, alerts961.txt, an hc message at most every 10 min); it never stops or kills anything.
WT=/home/nathan/Source/choptuik-large-d-961
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I961-dh370
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
T=10
PY=$WT/.venv/bin/python
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
# the low-memory recipe of the build (cargo test --release compiles the crate again)
export CARGO_BUILD_JOBS=6 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
cd $WT/hp || exit 9
log() { echo "961 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_961.txt; }

watch() {
  last=0
  while sleep 30; do
    now=$(date +%s)
    read -r used avail swap < <(free -m | awk '/^Mem:/{u=$3;a=$7} /^Swap:/{s=$3} END{print u,a,s}')
    procs=$(ps -eo rss=,pcpu=,comm=,args= | awk '($3 ~ /^python/ && /(anm_run|jet_by_order_check|series_split_check)\.py/) || $3 ~ /^(rustc|hpkernel)/ {printf "%s %d MB %s%% ", $3, $1/1024, $2}')
    echo "$(date -u '+%F %T') used ${used} avail ${avail} swap ${swap} load $(cut -d' ' -f1 /proc/loadavg) | ${procs}" >> $OUT/mem961.log
    if [ "$swap" -gt 6500 ] || [ "$avail" -lt 500 ]; then
      echo "$(date -u '+%F %T') ALERT swap ${swap} avail ${avail}" >> $OUT/alerts961.txt
      if [ $((now - last)) -ge 600 ]; then
        last=$now
        hc send nathans-macbook-air-m5-3/t5 "dh370 #961 memory alert: swap ${swap} MB, available ${avail} MB (watcher only logs, nothing stopped)" >/dev/null 2>&1
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
JBO="$PY -u jet_by_order_check.py $RAW"
# the flags of #960's P1 except --N, --ks and the a rule, which each step sets
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --keep_plan 0 --D_max 240 --steps 1"
step() {                          # step NAME DIR FLAGS...
  n=$1; d=$2; shift 2
  stage $n $OUT/$d.log timeout -s TERM 7200 $PY -u anm_run.py $RAW $OUT/$d --state $ST $CH "$@"
}

for s in "$@"; do
  case $s in
  test)
    stage cargo_test_oseries $OUT/cargo_test_oseries.log cargo test --release --lib oseries_ -- --nocapture --test-threads=1 || exit 1 ;;
  jbo)
    stage jbo10 $OUT/jbo10.log $JBO $ST --N 24 --threads $T --Np 6 --save $OUT/s10.npz --out $OUT/jbo10 || exit 1
    stage jbo4 $OUT/jbo4.log $JBO $ST --N 12 --threads 4 --Np 6 --compare $OUT/s10.npz --out $OUT/jbo4 || exit 1 ;;
  tf)
    stage tf1_ST $OUT/tf1_ST.log $JBO $ST --N 24 --threads $T --Np 6 --tangent_from 1 --out $OUT/tf1_ST || exit 1
    stage tf1_ST2 $OUT/tf1_ST2.log $JBO $ST2 --N 24 --threads $T --Np 6 --tangent_from 1 --out $OUT/tf1_ST2 || exit 1
    stage tf3_ST $OUT/tf3_ST.log $JBO $ST --N 24 --threads $T --Np 6 --tangent_from 3 --out $OUT/tf3_ST || exit 1 ;;
  split)
    stage split $OUT/split.log $PY -u series_split_check.py $RAW $ST --N 24 --threads $T --Np 6 --out $OUT/split || exit 1 ;;
  a) step step_off step_off --N 24 --ks 240 || exit 1 ;;
  b) step step_on step_on --N 24 --ks 240 --jet_tangent_from 1 --series_split 1 || exit 1 ;;
  c) step step_ks250 step_ks250 --N 24 --ks 250 || exit 1 ;;
  d) step step_n31 step_n31 --N 31 --ks 240 --jet_tangent_from 1 --series_split 1 --a_rule reseed --a_scale 0.0715 || exit 1 ;;
  delta)
    A=$(ls $OUT/step_off/anm_pin3_D*.npz 2>/dev/null | head -1); B=$(ls $OUT/step_on/anm_pin3_D*.npz 2>/dev/null | head -1)
    C=$(ls $OUT/step_ks250/anm_pin3_D*.npz 2>/dev/null | head -1)
    stage delta_b_a $OUT/delta_b_a.log $PY $OUT/delta_cmp961.py "$A" "$B" 1e-40 || exit 1
    stage delta_c_a $OUT/delta_c_a.log $PY $OUT/delta_cmp961.py "$A" "$C" 1e-40 --expect-above || exit 1 ;;
  *) log "unknown stage $s"; exit 3 ;;
  esac
done
log "stages $* done"
