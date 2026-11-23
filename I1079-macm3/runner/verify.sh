#!/bin/bash
# #1079 macm3b step 3 (the test): for each zero N = 1, 2 from main's solver/proof (a4cd5eaa), nice 10, 1 thread per BLAS:
#   krawczyk --box=data/A_M_box_M3xN_1e-10.json            (the verdict; NOT --hier, which compares with the fundamental zero's stored solves: not applicable, the coordinator's word)
#   if it exits 0: controls --box=... (exit 0 iff C0-C8 as expected), certify_M_recheck.py <box> (same verdict), certify_M_recheck.py <box> --mutate (must fail)
#   if it exits nonzero: the margins are in its log; the recheck (and its --mutate) is still run to see whether the independent assembly gives the same verdict; no controls, no --best, no --shrink (a smaller box needs the coordinator's word).
# Records in $P/steps.txt. A nonzero exit that is not expected writes a STOP line. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079
MAIN=a4cd5eaa7b297ffc6f171551fa15ba054e970e21
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = "$MAIN" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: the main worktree is not at $MAIN or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
run() {   # run NAME CMD...: output to logs/NAME.log; returns the exit code; records the command, the end and the last line
    local name=$1; shift
    echo "verify $name command: cd $W/solver/proof && nice -n 10 $PY $* > logs/$name.log 2>&1" >> $H
    nice -n 10 $PY "$@" > logs/$name.log 2>&1; local rc=$?
    echo "verify $name end $(stamp) exit $rc: $(tail -1 logs/$name.log | cut -c1-250)" >> $H
    return $rc
}
for n in 1 2; do
  BOX=data/A_M_box_M3x${n}_1e-10.json
  [ -f $BOX ] || { echo "$(stamp) STOP: $BOX is missing" >> $H; continue; }
  run A_M_krawczyk_M3x${n}_1e-10 certify_M.py krawczyk --box=$BOX; k=$?
  if [ $k = 0 ]; then
    run A_M_controls_M3x${n}_1e-10 certify_M.py controls --box=$BOX; c=$?
    [ $c = 0 ] || echo "$(stamp) STOP: controls x$n exit $c (0 expected)" >> $H
    run A_M_recheck_M3x${n}_1e-10 certify_M_recheck.py $BOX; r=$?
    [ $r = 0 ] || echo "$(stamp) STOP: recheck x$n exit $r (0 expected: the same verdict as krawczyk)" >> $H
    run A_M_recheck_M3x${n}_1e-10_mutate certify_M_recheck.py $BOX --mutate; m=$?
    [ $m != 0 ] || echo "$(stamp) STOP: recheck --mutate x$n exit 0 (must fail)" >> $H
  else
    echo "$(stamp) STOP: krawczyk x$n exit $k: the test does not pass at h 1e-10 (margins in logs/A_M_krawczyk_M3x${n}_1e-10.log); a smaller box needs the coordinator's word" >> $H
    run A_M_recheck_M3x${n}_1e-10 certify_M_recheck.py $BOX; r=$?
    run A_M_recheck_M3x${n}_1e-10_mutate certify_M_recheck.py $BOX --mutate; m=$?
  fi
done
echo "verify done $(stamp)" >> $H
exit 0
}
