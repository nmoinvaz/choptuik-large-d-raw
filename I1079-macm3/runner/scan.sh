#!/bin/bash
# #1079 macm3b round 2 (the coordinator's order after the diagnosis): (a) krawczyk --best on the two existing runs; (b) for each zero N in 1, 2 (side by side: 2 processes at a time) and each h in 1e-11 1e-12 1e-13, w in 1e-15 1e-14 1e-13 1e-12:
# box 3 --centre=data/A_M_refine_M3_xN.json --use_out --h=H --w=W, then krawczyk --box=... (no --hier); every box that passes gets controls --box=..., certify_M_recheck.py <box> and its --mutate.
# From main's solver/proof (worktree ~/Source/choptuik-large-d-1079 at a4cd5eaa), nice 10, 1 thread per BLAS. A box run that ends with an exception is recorded (NOTE) and not repeated; an unexpected result of a control or of the recheck is a STOP line.
# Records in $P/steps.txt. Own session under caffeinate -is.
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
run() {   # run NAME CMD...: output to logs/NAME.log, returns the exit code, records the command and the end
    local name=$1; shift
    echo "scan $name command: cd $W/solver/proof && nice -n 10 $PY $* > logs/$name.log 2>&1" >> $H
    nice -n 10 $PY "$@" > logs/$name.log 2>&1; local rc=$?
    echo "scan $name end $(stamp) exit $rc: $(tail -1 logs/$name.log | cut -c1-200)" >> $H
    return $rc
}
echo "scan start $(stamp)" >> $H
# (a)
for n in 1 2; do run A_M_krawczyk_M3x${n}_1e-10_best certify_M.py krawczyk --box=data/A_M_box_M3x${n}_1e-10.json --best; done
# (b)
one_zero() {
  local n=$1 h w tag box
  for h in 1e-11 1e-12 1e-13; do
    for w in 1e-15 1e-14 1e-13 1e-12; do
      tag=M3x${n}_h${h}_w${w}; box=data/A_M_box_$tag.json
      if [ -e $box ]; then echo "$(stamp) NOTE: $box exists, skipped" >> $H; continue; fi
      echo "scan box $tag start $(stamp)" >> $H
      run A_M_box_${tag}_stdout certify_M.py box 3 --centre=data/A_M_refine_M3_x$n.json --use_out --h=$h --w=$w --out=$box --log=logs/A_M_box_$tag.log; rc=$?
      if [ $rc != 0 ]; then echo "scan NOTE: box $tag ended with exit $rc (not repeated): $(tail -3 logs/A_M_box_${tag}_stdout.log | tr '\n' ' ' | cut -c1-300)" >> $H; continue; fi
      run A_M_krawczyk_$tag certify_M.py krawczyk --box=$box; k=$?
      echo "scan margins $tag exit $k: $(head -1 logs/A_M_krawczyk_$tag.log | cut -c1-200)" >> $H
      if [ $k = 0 ]; then
        run A_M_controls_$tag certify_M.py controls --box=$box; c=$?
        [ $c = 0 ] || echo "$(stamp) STOP: controls $tag exit $c (0 expected)" >> $H
        run A_M_recheck_$tag certify_M_recheck.py $box; r=$?
        [ $r = 0 ] || echo "$(stamp) STOP: recheck $tag exit $r (0 expected: the same verdict as krawczyk)" >> $H
        run A_M_recheck_${tag}_mutate certify_M_recheck.py $box --mutate; m=$?
        [ $m != 0 ] || echo "$(stamp) STOP: recheck --mutate $tag exit 0 (must fail)" >> $H
      fi
    done
  done
  echo "scan zero x$n done $(stamp)" >> $H
}
one_zero 1 &
one_zero 2 &
wait
echo "scan done $(stamp)" >> $H
exit 0
}
