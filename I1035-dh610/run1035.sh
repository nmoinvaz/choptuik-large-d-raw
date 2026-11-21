#!/bin/bash
# #1035 stage 2, the planted run at D 237.7132 (dh610; the coordinator's commands of 21 Nov, notes/FACTORED_HORIZON.md 5.3): selftests, then planted, planted_order (the control that must fail), and as information only planted_old and
# planted_linear, one after the other, nice 10, 10 threads, each capped at 7200 s by `timeout -s TERM` (TERM to its child). If planted does not exit 0 the script stops (no later run: the order control, the information runs
# and stage 3 do not run). Each run's log is read by check1035.py; a sampler logs the run's RSS, CPU, MemAvailable and the load every 60 s to rss_<run>.log. A braced block ending in exit.
{
RAW=/home/nathan/Source/choptuik-large-d-raw; WT=/home/nathan/Source/choptuik-large-d-1035; VENV=/home/nathan/Source/venv-i1058
D=$RAW/I1035-dh610; OUT=${OUT1035:-$D/stage2_planted}; SD=$D
P0=I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz; PR=I1064-dh170/p315/ks315/base_pin3_D237.7132.npz
mkdir -p $OUT
X=$OUT/exits_1035.txt; SUM=$OUT/summary_1035.txt
stamp() { date -u '+%F %T'; }
log() { echo "1035 $* $(stamp) UTC" >> $X; }
[ "$(git -C $WT rev-parse HEAD)" = bae00edf8262053122eaf03daadfd318da6a78eb ] || { log "worktree $WT is not at bae00edf8262053122eaf03daadfd318da6a78eb: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$P0)" = 861c79ff8ffc4b10067c487287ff46286b4ed4ba ] || { log "P0's blob is not 861c79ff8ffc4b10067c487287ff46286b4ed4ba: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$PR)" = 0f4858eef006333cd0356ee73a4c9eadccdaf6c0 ] || { log "PR's blob is not 0f4858eef006333cd0356ee73a4c9eadccdaf6c0: stop"; exit 1; }
log "worktree $WT at bae00edf, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), P0 861c79ff, PR 0f4858ee"
. $VENV/bin/activate
cd $SD; python3 -I check1035.py --selftest > check1035_selftest.txt 2>&1; c1=$?; python3 -I check1035.py --selftest --mutate > check1035_selftest_mutate.txt 2>&1; c2=$?
echo "check1035.py: selftest exit $c1 (0), --mutate exit $c2 (1)" >> $SUM; [ $c1 = 0 ] && [ $c2 = 1 ] || { log "check1035 controls wrong: stop"; exit 1; }
cd $WT/hp || exit 1
python3 factored_raise.py selftest $RAW/$P0 > $OUT/selftest.log 2>&1; s1=$?
python3 factored_raise.py selftest $RAW/$P0 --mutate=nopred > $OUT/selftest_nopred.log 2>&1; s2=$?
python3 -I $SD/check1035.py selftest-log $OUT/selftest.log $s1 >> $SUM 2>&1; k1=$?
python3 -I $SD/check1035.py nopred $OUT/selftest_nopred.log $s2 >> $SUM 2>&1; k2=$?
log "selftest exit $s1 (must be 0), nopred exit $s2 (must be 1), rules $k1/$k2"
[ $k1 = 0 ] && [ $k2 = 0 ] || { log "a selftest rule is not met: stop"; exit 1; }
run() {  # NAME KIND [extra args]
  local N=$1 K=$2; shift 2
  mkdir -p $OUT/$N
  local t0=$(date +%s) peak=0 pcpu=0 line
  ( timeout -s TERM 7200 nice -n 10 python3 -u factored_raise.py $RAW $OUT/$N --state $P0 --ks 315 --threads 10 --ref $PR --bar 1e-60 "$@" > $OUT/$N.log 2>&1; echo $? > $OUT/$N.rc ) &
  local bg=$!
  log "$N started (extra args: ${*:-none}), subshell $bg"
  while kill -0 $bg 2>/dev/null; do
    line=$(ps -eo pid=,pcpu=,rss=,etime=,args= | grep -F "factored_raise.py $RAW $OUT/$N " | grep -v -e grep -e timeout -e nice | head -1)
    if [ -n "$line" ]; then
      set -- $line; [ "$3" -gt "$peak" ] && peak=$3; pcpu=$2
      echo "$(stamp) UTC pid $1 pcpu $2 rss_kB $3 etime $4 memavail_kB $(awk '/^MemAvailable/ {print $2}' /proc/meminfo) load $(cut -d' ' -f1 /proc/loadavg)" >> $OUT/rss_$N.log
    fi
    sleep 60
  done
  wait $bg; local rc; rc=$(cat $OUT/$N.rc); local w=$(( $(date +%s) - t0 ))
  log "$N exit $rc wall ~$w s, peak sampled RSS $peak kB, last pcpu $pcpu"
  echo "$N: exit $rc, wall ~$w s (60 s samples), peak sampled RSS $peak kB, last pcpu $pcpu" >> $SUM
  python3 -I $SD/check1035.py $K $OUT/$N.log $rc >> $SUM 2>&1; CK=$?
  log "$N check ($K) rule exit $CK"
  RC=$rc
}
run planted planted
if [ "$RC" != 0 ]; then log "planted did not exit 0 (exit $RC): stop, no later run; push planted.log and planted/raise.json or lastiter_*.npz"; echo "planted failed: stopped" >> $SUM; log "done"; exit 0; fi
run planted_order order
run planted_old planted --mutate=old       # information only
run planted_linear planted --mutate=linear # information only
log "done"
echo "1035 stage 2 planted done" >> $SUM
exit 0
}
