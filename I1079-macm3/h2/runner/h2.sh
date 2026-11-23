#!/bin/bash
# #1079 macm3b H2 (the coordinator's order after H1 and H3): lemma6b1_cover_M.py at an excited centre, M = 3, --h=1e-11, --tag=_excN, --x=<p^>.
# usage: bash h2.sh STAGE N   (N = 1: x1, the box M3x1E2_h1e-12_w1e-13, tag _exc1; N = 2: x2, the box M3x2E2_h1e-12_w1e-12, tag _exc2)
#   STAGE pilot : probe (process A) beside ray --c1 then row --j=11 (process B); resumes the ray with --resume when the run folder has a ray.json
#   STAGE rowsA / rowsB : rows --only=0,2,4,6,8,10 / --only=1,3,5,7,9 (the other 11 rows over two processes)
#   STAGE check : check --json=lemmas_M_runs/lemma6b1_check_M3_excN.json, c1check, mutate --j=11
# From the worktree ~/Source/choptuik-large-d-1079f (feat/certify-excited 89553c6b), solver/proof; nice 10, 1 thread per BLAS. Records in $P/steps_h2.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
WB=/Users/nathan/Source/choptuik-large-d-1079e
W=/Users/nathan/Source/choptuik-large-d-1079f
BR=89553c6b1645c1a5711a4d17fb71306963b963a7
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps_h2.txt
ST=$1; N=$2
case $N in
  1) BOX=M3x1E2_h1e-12_w1e-13 ;;
  2) BOX=M3x2E2_h1e-12_w1e-12 ;;
  *) echo "$(date -u '+%F %T') STOP: h2 unknown zero $N" >> $H; exit 1 ;;
esac
TAG=_exc$N
stamp() { date -u '+%F %T'; }
note() { echo "h2 $ST exc$N $(stamp) $*" >> $H; }
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: h2 $ST exc$N: the worktree $W is not at $BR or has tracked changes" >> $H; exit 1; }
XP=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p"]))' $WB/solver/proof/data/A_M_box_$BOX.json) || { echo "$(stamp) STOP: h2 exc$N: cannot read the box" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
mkdir -p logs lemmas_M_runs
COM="--M=3 --x=$XP --h=1e-11 --tag=$TAG"
run() {   # run NAME CMD ARGS...: output to logs/NAME.log (appended), returns the exit code
    local name=$1; shift
    note "$name command: cd $W/solver/proof && nice -n 10 $PY -u lemma6b1_cover_M.py $1 --M=3 --x=<p^ of $BOX> --h=1e-11 --tag=$TAG ${*:2} > logs/$name.log 2>&1"
    local t0=$(date +%s)
    nice -n 10 $PY -u lemma6b1_cover_M.py "$1" $COM "${@:2}" >> logs/$name.log 2>&1; local rc=$?
    note "$name end exit $rc, $(( $(date +%s) - t0 )) s: $(tail -1 logs/$name.log | cut -c1-220)"
    return $rc
}
note "start: box $BOX; python-flint $($PY -c 'import flint; print(flint.__version__, "FLINT", flint.__FLINT_VERSION__)'), $($PY -V 2>&1); p^ = $XP"
case $ST in
  pilot)
    ( run I1079_h2_probe_exc$N probe ; echo "h2 pilot exc$N $(stamp) process A (probe) done" >> $H ) &
    ( RES=""; [ -f lemma6b1_runs_M3$TAG/ray.json ] && RES="--resume"
      run I1079_h2_ray_exc$N ray --c1 $RES; r=$?
      if [ $r = 0 ]; then run I1079_h2_row11_exc$N row --j=11; r2=$?; else echo "$(stamp) STOP: h2 pilot exc$N: ray --c1 exit $r (cause in logs/I1079_h2_ray_exc$N.log)" >> $H; fi
      echo "h2 pilot exc$N $(stamp) process B (ray, row 11) done" >> $H ) &
    wait; note "pilot done" ;;
  rowsA) run I1079_h2_rowsA_exc$N rows --only=0,2,4,6,8,10; note "rowsA done" ;;
  rowsB) run I1079_h2_rowsB_exc$N rows --only=1,3,5,7,9; note "rowsB done" ;;
  check)
    run I1079_h2_check_exc$N check --json=lemmas_M_runs/lemma6b1_check_M3_exc$N.json; c=$?
    run I1079_h2_c1check_exc$N c1check; d=$?
    run I1079_h2_mutate_exc$N mutate --j=11; m=$?
    note "check exit $c (0/PASS wanted), c1check exit $d (0 wanted), mutate --j=11 exit $m: $(tail -1 logs/I1079_h2_mutate_exc$N.log | cut -c1-200)"
    note "check done" ;;
  *) echo "$(stamp) STOP: h2 unknown stage $ST" >> $H; exit 1 ;;
esac
exit 0
}
