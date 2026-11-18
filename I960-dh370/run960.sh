#!/usr/bin/env bash
# #960, the kernel pilots of anm_run.py --a_rule reseed (the issue's commands as written; T = 10, the build is the worktree -957's).
# usage: bash run960.sh STAGE...    stages: p0 p1 p2 bits. A Traceback in a stage's log stops the list; a non-zero exit alone does not
# (a pilot FAIL is a result). The watcher only logs and alerts.
WT=/home/nathan/Source/choptuik-large-d-957
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I960-dh370
L=I903-win2/ks_chain/leg07_D222.0000_ks240
T=10
PY=$WT/.venv/bin/python
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$PATH PYTHONFAULTHANDLER=1
cd $WT/hp || exit 9
log() { echo "960 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_960.txt; }

watch() {
  last=0
  while sleep 30; do
    now=$(date +%s)
    read -r used avail swap < <(free -m | awk '/^Mem:/{u=$3;a=$7} /^Swap:/{s=$3} END{print u,a,s}')
    procs=$(ps -eo rss=,pcpu=,comm=,args= | awk '$3 ~ /^python/ && /(anm_run|step_rule_check)\.py/ {printf "%d MB %s%% ", $1/1024, $2}')
    echo "$(date -u '+%F %T') used ${used} avail ${avail} swap ${swap} load $(cut -d' ' -f1 /proc/loadavg) | ${procs}" >> $OUT/mem960.log
    if [ "$swap" -gt 6500 ] || [ "$avail" -lt 500 ]; then
      echo "$(date -u '+%F %T') ALERT swap ${swap} avail ${avail}" >> $OUT/alerts960.txt
      if [ $((now - last)) -ge 600 ]; then
        last=$now
        hc send nathans-macbook-air-m5-3/t5 "dh370 #960 memory alert: swap ${swap} MB, available ${avail} MB (watcher only logs, nothing stopped)" >/dev/null 2>&1
      fi
    fi
  done
}

stage() {                         # stage NAME LOG CMD...
  name=$1; lg=$2; shift 2
  log "$name start"
  t=$(date +%s)
  "$@" >> $lg 2>&1
  rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t ))s"
  if grep -q '^Traceback' $lg; then log "$name Traceback in $(basename $lg), stop"; return 99; fi
  return 0
}

watch & WP=$!
trap 'kill $WP 2>/dev/null' EXIT
{ echo "hpkernel: $($PY -c 'import hpkernel; print(hpkernel.__file__, hpkernel._hpkernel.__file__)')"
  echo "worktree: $(git -C $WT rev-parse HEAD)"; echo "python: $($PY -V)"; echo "date: $(date -u '+%F %T UTC')"; } >> $OUT/build960.txt
SRC="nice -n 10 $PY -u step_rule_check.py pilot $RAW"

for s in "$@"; do
  case $s in
  p0)
    stage p0a $OUT/p0a.log $SRC --jet $L/jet_pin3_D229.0509.npz --state $L/anm_pin3_D229.0509.npz --N 24 \
      --as 0.70 --refuse 0.9313225746154785,1.0 --scale 0.0715 --threads $T --out $OUT/pilot_n24_D229.jsonl || exit 1
    stage p0b $OUT/p0b.log $SRC --jet $L/jet_pin3_D230.5643.npz --state $L/anm_pin3_D230.5643.npz --N 24 \
      --as 0.66,0.70,0.7275957614183426 --scale 0.0715 --threads $T --out $OUT/pilot_n24_D230.jsonl || exit 1 ;;
  p1)
    stage p1 $OUT/p1.log nice -n 10 timeout -s TERM 10800 $PY -u anm_run.py $RAW $OUT/n31 --state $L/anm_pin3_D229.0509.npz \
      --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 \
      --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural \
      --save_jet 1 --od_strong 4 --reseed_start pred --ks 240 --keep_plan 0 --D_max 240 --steps 1 --a_rule reseed --a_scale 0.0715 \
      || exit 1 ;;
  p2)
    J=I960-dh370/n31/jet_pin3_D229.0509.npz
    [ -f $RAW/$J ] || { log "p2 missing $J, not run"; exit 2; }
    stage p2 $OUT/p2.log $SRC --jet $J --state $L/anm_pin3_D229.0509.npz --N 31 --as 0.75,1.0,1.15,1.25,1.4 --scale 0.0715 \
      --threads $T --out $OUT/pilot_n31.jsonl || exit 1 ;;
  bits)
    # default bits on the chain path: origin/main's anm_run.py (copied in as anm_run_main.py, untracked) against the branch's, the
    # chain's F of I903-win2/run_ks_chain.sh with --threads $T, --steps 1 from the same state
    git -C $WT show origin/main:hp/anm_run.py > $WT/hp/anm_run_main.py && cp $WT/hp/anm_run_main.py $OUT/anm_run_main.py
    log "bits: anm_run_main.py = origin/main $(git -C $WT rev-parse --short origin/main), sha1 $(sha1sum < $OUT/anm_run_main.py | cut -c1-12); anm_run.py sha1 $(sha1sum < $WT/hp/anm_run.py | cut -c1-12)"
    FB="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads $T --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
    for v in anm_run_main anm_run; do
      stage bits_$v $OUT/bits_$v.log nice -n 10 timeout -s TERM 10800 $PY -u $v.py $RAW $OUT/bits_$v --state $L/anm_pin3_D229.0509.npz \
        $FB --ks 240 --keep_plan 0 --D_max 240 --steps 1 || exit 1
    done
    $PY $OUT/bits_cmp960.py $OUT/bits_anm_run_main $OUT/bits_anm_run > $OUT/bits_cmp.log 2>&1; log "bits compare exit $?" ;;
  *) log "unknown stage $s"; exit 3 ;;
  esac
done
log "stages $* done"
