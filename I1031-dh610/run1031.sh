#!/bin/bash
# #1031 on dh610: hp's cols_ cargo test at main 5d0a96e6, without RUSTFLAGS and with -C target-cpu=native; each run capped at 3 x its estimate
# (estimate 15 min each from #1009's 575 s and 969 s under load; cap 45 min by timeout on cargo's exact pid). One line per run in summary_1031.txt.
. "$(dirname "$0")/common1031.sh"
export CARGO_BUILD_JOBS=6 OMP_NUM_THREADS=1
SUM=$OUT/summary_1031.txt
. $VENV/bin/activate
cd "$WT/hp" || exit 1
H=5d0a96e6
[ "$(git rev-parse HEAD | cut -c1-8)" = $H ] || { echo "WT is not at $H"; exit 1; }
[ -z "$(git status --short)" ] || { echo "worktree not clean"; exit 1; }
echo "# $(stamp) UTC start, hp $(git rev-parse --short=8 HEAD), $(cargo --version), $(rustc --version), multidouble $(grep -A1 'name = "multidouble"' Cargo.lock | sed -n 2p), load $(cut -d' ' -f1-3 /proc/loadavg), CPU $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)" > $SUM
one() {   # one NAME RUSTFLAGS
  local name=$1 rf=$2 s=$(date +%s)
  { echo "# $(stamp) UTC cmd: RUSTFLAGS='$rf' cargo test --profile release-dev --lib cols_ -- --nocapture"; } > $OUT/$name.log
  RUSTFLAGS="$rf" nice -n 10 timeout -s TERM 2700 cargo test --profile release-dev --lib cols_ -- --nocapture >> $OUT/$name.log 2>&1 &
  local pid=$!
  bash $OUT/watch1031.sh $pid $OUT/mem_$name.log 30 &
  wait $pid; local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  local wall=$(( $(date +%s) - s ))
  local ok=$(grep -c "^test result: ok. 2 passed" $OUT/$name.log)
  local cmp=$(grep -c "333000 entries compared, none differ" $OUT/$name.log)
  local nl=$(grep -cE "entries differ \(parallel: 0\); control: [0-9]+ differ" $OUT/$name.log)
  local bad=$(grep -E "entries differ \(parallel: 0\); control: [0-9]+ differ" $OUT/$name.log | grep -vcE "^ *M [0-9]+ .*: 0 of [0-9]+ entries differ \(parallel: 0\); control: [1-9][0-9]* differ")
  local be=$(grep -oE 'backend::[A-Za-z0-9]+' $OUT/$name.log | sort | uniq -c | tr -s ' ' | tr '\n' ';')
  echo "$name (RUSTFLAGS '$rf'): expected exit 0, got $rc, $wall s $([ $rc = 0 ] && echo OK || echo MISMATCH); '2 passed' lines $ok (1), '333000 none differ' lines $cmp (1), tile lines $nl (22), tile lines not '0 differ with control > 0' $bad (0); backends: $be; peak $(tail -1 $OUT/mem_$name.log | grep -o 'peak tree rss [0-9]* MiB')" >> $SUM
}
one cols_test ""
one cols_test_native "-C target-cpu=native"
echo "# $(stamp) UTC done" >> $SUM
