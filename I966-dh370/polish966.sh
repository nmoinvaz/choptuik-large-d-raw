#!/usr/bin/env bash
# #966 discriminating polishes (coordinator's hc, 2026-11-18 ~20:25 UTC): the leg 0 polish of ks_chain3, ks 291 to 304 from ks_chain2's D 237.7132 state, with
# run903e.sh's old flags (N 24, h_max 1.0, qd_it 20, a_grow 1.25 a_hold 1, no a rule, no tangent, no split) at --threads 5, on two builds side by side:
#   main  the -961 venv and hp/anm_run.py of 40f4b4a5, OUT I966-dh370/polish_main_old
#   957   the -957 venv and hp/anm_run.py of 954eadcb (no #953, no #955, multidouble 4.8.2), OUT I966-dh370/polish_957_old
# Command as run903d.sh's rungs: anm_run.py RAW OUT --state S F --steps 0 --ks 304 --keep_plan 0 --save_base 1, 2 h cap each (timeout), 5 threads at nice 10 each.
# The watcher only logs and alerts (mem966.log, alerts966.txt, hc at most every 10 min); it never stops or kills anything.
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I966-dh370
S=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
# run903e.sh's F, copied from raw (a copy of the file is in this folder), with the threads set to 5
F=$(sed -n 's/^F="\(.*\)"$/\1/p' $OUT/run903e.sh | sed 's/--threads 9/--threads 5/')
[ -n "$F" ] || { echo "no F in run903e.sh"; exit 8; }
export PYTHONFAULTHANDLER=1 PATH=$HOME/.local/bin:$PATH
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }

watch() {
  last=0
  while sleep 30; do
    now=$(date +%s)
    read -r used avail swap < <(free -m | awk '/^Mem:/{u=$3;a=$7} /^Swap:/{s=$3} END{print u,a,s}')
    procs=$(ps -eo rss=,pcpu=,comm=,args= | awk '$3 ~ /^python/ && /anm_run\.py/ {printf "%s %d MB %s%% ", $3, $1/1024, $2}')
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

run() {                           # run NAME WORKTREE
  name=$1; wt=$2; out=$OUT/$name; mkdir -p $out
  lg=$out/anm_run.log
  echo "== $name $(date -u '+%F %T') $(git -C $wt rev-parse --short HEAD) $wt/hp anm_run.py $RAW $out --state $S $F --steps 0 --ks 304 --keep_plan 0 --save_base 1" > $lg
  log "$name start (worktree $(basename $wt) $(git -C $wt rev-parse --short HEAD))"
  t=$(date +%s)
  ( cd $wt/hp && VIRTUAL_ENV=$wt/.venv PATH=$wt/.venv/bin:$PATH nice -n 10 timeout -s TERM 7200 $wt/.venv/bin/python -u anm_run.py $RAW $out --state $S $F --steps 0 --ks 304 --keep_plan 0 --save_base 1 ) >> $lg 2>&1
  rc=$?
  echo "exit $rc" >> $lg
  log "$name exit $rc wall $(( $(date +%s) - t ))s base $(ls $out/base_pin*_D*.npz 2>/dev/null | head -1 | xargs -r basename)"
  grep -q '^Traceback' $lg && log "$name Traceback in its log"
}

watch & WP=$!
trap 'kill $WP 2>/dev/null' EXIT
run polish_main_old /home/nathan/Source/choptuik-large-d-961 &
run polish_957_old /home/nathan/Source/choptuik-large-d-957 &
wait
log "polishes done"
