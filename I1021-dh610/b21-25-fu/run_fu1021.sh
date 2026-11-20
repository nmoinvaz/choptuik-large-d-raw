#!/bin/bash
# #1021 follow-ups of boxes 21-25 (dh610) at wip/argcount-m3-bounds 6da7da7b, steps in the coordinator's order 2, 1, 3:
#   run_fu1021.sh 0 2 1 3     0: the selftests (argcount plain, seedfix, nocap, lowcap exits 0 1 1 1; fu_value.py selftest and
#                              its --break control exits 0 1); 2, 1, 3: the steps (cells_step<S>.jsonl)
# A step passes: value the points without value in its unresolved cells again (fu_value.py, six variants, 3 processes), then
# recount the cells with --retry at xi1 0.17 (located zeros again at 0.18), 3 processes; the next pass takes the unresolved
# leaves of the last one; it ends when none are left, when a pass leaves its cells unchanged, or after 3 passes. At most 4
# processes (the main process and 3 workers), nice 10, one job at a time.
set -u
CODE=/home/nathan/Source/choptuik-1021-seed; PY=/home/nathan/Source/venv-i1026/bin/python
RAW=/home/nathan/Source/choptuik-large-d-raw-1021; OUT=$RAW/I1021-dh610/b21-25-fu
H=6da7da7be3f2325208f2d4f9570a5e5a8790bd78
X=$OUT/exits_fu.txt; st() { date -u '+%F %T'; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = $H ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git status --short)" ] || { echo "worktree not clean"; exit 1; }
G="nice -n 10 timeout -s TERM"

same_cells() {   # same_cells A.jsonl B.jsonl: 0 when the unresolved cells of both are the same set
  $PY - "$1" "$2" <<'E'
import json, sys
c = lambda f: {(round(l["a0"], 9), round(l["a1"], 9), round(l["w0"], 9), round(l["w1"], 9)) for l in map(json.loads, open(f)) if not l["ok"]}
sys.exit(0 if c(sys.argv[1]) == c(sys.argv[2]) else 1)
E
}
unresolved() { $PY -c "import json,sys;print(sum(1 for l in map(json.loads,open(sys.argv[1])) if not l['ok']))" "$1"; }

step() {
  S=$1; RC=$2
  IN=$OUT/cells_step$S.jsonl
  for P in 1 2 3; do
    T=step${S}_pass$P
    echo "$T value start $(st), cells $(unresolved $IN)" >> $X
    $G 10800 $PY -u $OUT/fu_value.py $CODE $OUT/points_M3_r0.17.jsonl $OUT/rows_$T.jsonl --auto $IN --procs 3 --append \
        > $OUT/logs/value_$T.log 2>&1
    echo "$T value exit $? (0: all points accepted, 2: some stay unvalued) $(st)" >> $X
    for m in f3 lowguard; do
      $PY $OUT/fu_value.py $CODE $OUT/points_M3_r0.17.jsonl $OUT/retest_${m}_$T.jsonl --retest $OUT/rows_$T.jsonl --mutate $m \
          > $OUT/logs/retest_${m}_$T.log 2>&1
      echo "$T retest --mutate=$m exit $? (1: the control fired)" >> $X
    done
    echo "$T recount start $(st)" >> $X
    $G $RC $PY -u argcount.py --M=3 --recount=$IN --r1=0.17 --r1b=0.18 --seed=$OUT/seeds_b21-25_r0.2.jsonl --m3fix --retry \
        --m3maxrhs=1e7 --m3wall=3600 --m3noisecap=1e7 --procs=3 --out=$OUT --tag=fu_$T > $OUT/logs/recount_$T.log 2>&1
    echo "$T recount exit $? $(st)" >> $X
    NEXT=$OUT/leaves_fu_$T.jsonl
    [ -s "$NEXT" ] || { echo "$T no leaves file" >> $X; return 1; }
    n=$(unresolved $NEXT)
    echo "$T unresolved cells $n, accepted rows $(grep -c ' accepted True' $OUT/logs/value_$T.log)" >> $X
    [ "$n" = 0 ] && { echo "step $S done: no unresolved cell $(st)" >> $X; return 0; }
    same_cells $IN $NEXT && { echo "step $S ends: pass $P left its cells unchanged $(st)" >> $X; return 0; }
    IN=$NEXT
  done
  echo "step $S ends after 3 passes, $(unresolved $IN) unresolved cells $(st)" >> $X
}

for s in "$@"; do
  case $s in
    0)
      echo "start $(st) code $(git rev-parse --short=8 HEAD) python $($PY -V) $($PY -c 'import numpy,scipy,mpmath;print(numpy.__version__,scipy.__version__,mpmath.__version__)')" >> $X
      E=""
      for m in "" seedfix nocap lowcap; do
        nice -n 10 $PY -u argcount.py --selftest ${m:+--mutate=$m} >> $OUT/logs/selftest_6da7da7b.log 2>&1; E="$E$? "
      done
      echo "selftest 6da7da7b plain seedfix nocap lowcap exits: $E" >> $X
      [ "$E" = "0 1 1 1 " ] || exit 1
      $PY $OUT/fu_value.py $CODE --selftest >> $OUT/logs/selftest_fu.log 2>&1; e1=$?
      $PY $OUT/fu_value.py $CODE --selftest --break >> $OUT/logs/selftest_fu.log 2>&1; e2=$?
      echo "fu_value selftest, --break exits: $e1 $e2 (0 1)" >> $X
      [ "$e1 $e2" = "0 1" ] || exit 1;;
    2) step 2 21600;;       # recount cap 6 h per pass (estimate 2 h)
    1) step 1 54000;;       # 15 h (estimate 5 h)
    3) step 3 32400;;       # 9 h (estimate 3 h)
  esac
done
echo "end $(st)" >> $X
