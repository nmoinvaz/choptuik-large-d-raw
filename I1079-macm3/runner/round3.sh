#!/bin/bash
# #1079 macm3b round 3 (the coordinator's order after round 2): (1) certify_M.py point 3 --p=<p_out of data/A_M_refine_M3_xN.json> --out=data/A_M_point_M3xN.json --log=logs/A_M_point_M3xN.log, N = 1 and 2 at a time;
# (2) krawczyk --box=<box> --point=data/A_M_point_M3xN.json for the 12 round-2 boxes per zero (and the 1e-10 run as an extra), no --hier; (3) for every box that passes: controls --box --point, certify_M_recheck.py <box> (it has no --point) and its --mutate.
# From main's solver/proof (worktree ~/Source/choptuik-large-d-1079 at a4cd5eaa), nice 10, 1 thread per BLAS. Records in $P/steps.txt. Own session under caffeinate -is.
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
    echo "round3 $name command: cd $W/solver/proof && nice -n 10 $PY $* > logs/$name.log 2>&1" >> $H
    nice -n 10 $PY "$@" > logs/$name.log 2>&1; local rc=$?
    echo "round3 $name end $(stamp) exit $rc: $(tail -1 logs/$name.log | cut -c1-220)" >> $H
    return $rc
}
echo "round3 start $(stamp)" >> $H
for n in 1 2; do
  [ ! -e data/A_M_point_M3x$n.json ] || { echo "$(stamp) STOP: data/A_M_point_M3x$n.json exists" >> $H; exit 1; }
  PS[$n]=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' data/A_M_refine_M3_x$n.json) || { echo "$(stamp) STOP: cannot read data/A_M_refine_M3_x$n.json" >> $H; exit 1; }
  echo "round3 point x$n p = ${PS[$n]}" >> $H
done
echo "round3 point runs start $(stamp)" >> $H
( run A_M_point_M3x1_stdout certify_M.py point 3 --p=${PS[1]} --out=data/A_M_point_M3x1.json --log=logs/A_M_point_M3x1.log; rc=$?
  [ $rc = 0 ] || echo "round3 NOTE: point run x1 exit $rc" >> $H ) &
( run A_M_point_M3x2_stdout certify_M.py point 3 --p=${PS[2]} --out=data/A_M_point_M3x2.json --log=logs/A_M_point_M3x2.log; rc=$?
  [ $rc = 0 ] || echo "round3 NOTE: point run x2 exit $rc" >> $H ) &
wait
for n in 1 2; do
  [ -f data/A_M_point_M3x$n.json ] || { echo "$(stamp) STOP: point run x$n produced no json" >> $H; exit 1; }
  echo "round3 point x$n g radius: $($PY -I -c 'import json, sys; r = json.load(open(sys.argv[1])); print("g_rad %.3e Dg_rad %.3e steps %s sec %.0f" % (r["g_rad"], r["Dg_rad"], r["steps"], r["sec"]))' data/A_M_point_M3x$n.json)" >> $H
done
for n in 1 2; do
  for h in 1e-11 1e-12 1e-13; do
    for w in 1e-15 1e-14 1e-13 1e-12; do
      tag=M3x${n}_h${h}_w${w}; box=data/A_M_box_$tag.json
      [ -f $box ] || { echo "round3 NOTE: $box is missing" >> $H; continue; }
      run A_M_krawczyk_pt_$tag certify_M.py krawczyk --box=$box --point=data/A_M_point_M3x$n.json; k=$?
      echo "round3 margins $tag exit $k: $(head -1 logs/A_M_krawczyk_pt_$tag.log | cut -c1-200)" >> $H
      if [ $k = 0 ]; then
        run A_M_controls_pt_$tag certify_M.py controls --box=$box --point=data/A_M_point_M3x$n.json; c=$?
        [ $c = 0 ] || echo "$(stamp) STOP: controls $tag exit $c (0 expected)" >> $H
        run A_M_recheck_pt_$tag certify_M_recheck.py $box; r=$?
        echo "round3 recheck $tag (no --point option) exit $r" >> $H
        run A_M_recheck_pt_${tag}_mutate certify_M_recheck.py $box --mutate; m=$?
        [ $m != 0 ] || echo "$(stamp) STOP: recheck --mutate $tag exit 0 (must fail)" >> $H
      fi
    done
  done
  tag=M3x${n}_1e-10; run A_M_krawczyk_pt_$tag certify_M.py krawczyk --box=data/A_M_box_$tag.json --point=data/A_M_point_M3x$n.json; k=$?
  echo "round3 margins $tag exit $k (extra: the 1e-10 run): $(head -1 logs/A_M_krawczyk_pt_$tag.log | cut -c1-200)" >> $H
done
echo "round3 done $(stamp)" >> $H
exit 0
}
