#!/bin/bash
# #1035 stage 2, the order control rerun (dh610): run1035.sh ran `run planted_order order` WITHOUT --mutate=order (my omission: the log's state line read 'ks 307 -> 315' and the run passed, which check1035.py reported as
# 'state line missing'), so that run is kept as planted_order_NOMUTATE and this script runs the control as ordered, `--mutate=order` (the raise to ks 314 against the ks 315 reference, which must fail), after unit i1035a has ended
# (the thread budget). The preflight (worktree, blobs) is as in run1035.sh; the selftests are not repeated. A braced block ending in exit.
{
RAW=/home/nathan/Source/choptuik-large-d-raw; WT=/home/nathan/Source/choptuik-large-d-1035; VENV=/home/nathan/Source/venv-i1058
D=$RAW/I1035-dh610; OUT=${OUT1035:-$D/stage2_planted}; SD=$D
P0=I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz; PR=I1064-dh170/p315/ks315/base_pin3_D237.7132.npz
mkdir -p $OUT
while [ "$(systemctl --user is-active i1035a)" = active ]; do sleep 20; done
X=$OUT/exits_1035.txt; SUM=$OUT/summary_1035_order_rerun.txt
stamp() { date -u '+%F %T'; }
log() { echo "1035 $* $(stamp) UTC" >> $X; }
[ "$(git -C $WT rev-parse HEAD)" = bae00edf8262053122eaf03daadfd318da6a78eb ] || { log "worktree $WT is not at bae00edf8262053122eaf03daadfd318da6a78eb: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$P0)" = 861c79ff8ffc4b10067c487287ff46286b4ed4ba ] || { log "P0's blob is not 861c79ff8ffc4b10067c487287ff46286b4ed4ba: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$PR)" = 0f4858eef006333cd0356ee73a4c9eadccdaf6c0 ] || { log "PR's blob is not 0f4858eef006333cd0356ee73a4c9eadccdaf6c0: stop"; exit 1; }
log "worktree $WT at bae00edf, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), P0 861c79ff, PR 0f4858ee"
. $VENV/bin/activate
cd $SD; python3 -I check1035.py --selftest > check1035_selftest_b.txt 2>&1; c1=$?; python3 -I check1035.py --selftest --mutate > check1035_selftest_mutate_b.txt 2>&1; c2=$?
echo "check1035.py (rerun): selftest exit $c1 (0), --mutate exit $c2 (1)" >> $SUM; [ $c1 = 0 ] && [ $c2 = 1 ] || { log "check1035 controls wrong: stop"; exit 1; }
cd $WT/hp || exit 1
run() {  # NAME KIND [extra args]
  local N=$1 K=$2; shift 2
  mkdir -p $OUT/$N
  local t0=$(date +%s) peak=0 pcpu=0 line
  local CMD=(timeout -s TERM 7200 nice -n 10 python3 -u factored_raise.py $RAW $OUT/$N --state $P0 --ks 315 --threads 10 --ref $PR --bar 1e-60 "$@")
  # the coordinator asked (21 Nov) for the command to be diffed against his before each launch, the diff kept: empty or not, it goes to cmddiff_$N.txt and the exits log, and a diff stops the launch
  python3 -I $SD/cmddiff1035.py $N --actual "${CMD[*]}" > $OUT/cmddiff_$N.txt 2>&1; local cd=$?
  log "$N command diff against the coordinator's: $(tail -1 $OUT/cmddiff_$N.txt) (exit $cd)"
  [ $cd = 0 ] || { log "$N: the command differs from the coordinator's: not launched"; RC=99; return; }
  ( "${CMD[@]}" > $OUT/$N.log 2>&1; echo $? > $OUT/$N.rc ) &
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
run planted_order order --mutate=order
log "done"
echo "1035 stage 2 order control rerun done" >> $SUM
exit 0
}
