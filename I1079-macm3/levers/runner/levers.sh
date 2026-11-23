#!/bin/bash
# #1079 macm3b levers (the coordinator's order, hc 2026-11-23 ~16:00 UTC): at one zero (x1 or x2) and one setting (E1: CERTIFY_M_XI1=0.2; E2: CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16; E3: both):
# refine 3 --p=<p> --iters=3 (stop if A or wf moves > 1e-8 from zero_mp's values), point run (g radius), 4 box runs (h in 1e-11 1e-12, w in 1e-13 1e-12), krawczyk --point (no --hier); for a box that passes: controls --point, certify_M_recheck.py and --mutate.
# usage: bash levers.sh SETTING ZERO   From the clean worktree of feat/certify-excited (1addcada), solver/proof; nice 10, 1 thread per BLAS. Records in $P/steps_levers.txt. Own session under caffeinate -is.
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079e
BR=1addcada42157c197ad1193621b988a978bb96f7
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps_levers.txt
S=$1; Z=$2; T=${Z}${S}
stamp() { date -u '+%F %T'; }
note() { echo "levers $T $(stamp) $*" >> $H; }
case $S in
  E1) export CERTIFY_M_XI1=0.2 ;;
  E2) export CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 ;;
  E3) export CERTIFY_M_XI1=0.2 CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 ;;
  *) echo "$(stamp) STOP: unknown setting $S" >> $H; exit 1 ;;
esac
case $Z in
  x2) PP=3.526473056695715,0.211497981391215,0.9765085451976188,-0.0017633195225818952; A0=3.526473056695715; W0=0.211497981391215 ;;
  x1) PP=3.446218246366727,0.347606965217407,0.8054175863852927,0.011780043848505818; A0=3.446218246366727; W0=0.347606965217407 ;;
  *) echo "$(stamp) STOP: unknown zero $Z" >> $H; exit 1 ;;
esac
[ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: $T: the worktree is not at $BR or has tracked changes" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
run() {   # run NAME CMD...: output to logs/NAME.log, returns the exit code, records the command and the end
    local name=$1; shift
    note "$name command: cd $W/solver/proof && nice -n 10 env XI1=${CERTIFY_M_XI1:-0.3(default)} NTAY=${CERTIFY_M_NTAY:-20(default)} NJAC=${CERTIFY_M_NJAC:-12(default)} $PY $* > logs/$name.log 2>&1"
    nice -n 10 $PY "$@" > logs/$name.log 2>&1; local rc=$?
    note "$name end exit $rc: $(tail -1 logs/$name.log | cut -c1-200)"
    return $rc
}
note "start: setting $S (CERTIFY_M_XI1=${CERTIFY_M_XI1:-unset} CERTIFY_M_NTAY=${CERTIFY_M_NTAY:-unset} CERTIFY_M_NJAC=${CERTIFY_M_NJAC:-unset}), zero $Z, p = $PP"
[ ! -e data/A_M_refine_M3_$T.json ] || { note "STOP: data/A_M_refine_M3_$T.json exists"; echo "$(stamp) STOP: $T refine json exists" >> $H; exit 1; }
run A_M_refine_M3_${T}_stdout certify_M.py refine 3 --p=$PP --iters=3 --tag=$T; rc=$?
[ $rc = 0 ] || { echo "$(stamp) STOP: $T refine exit $rc: $(tail -3 logs/A_M_refine_M3_${T}_stdout.log | tr '\n' ' ' | cut -c1-400)" >> $H; exit 1; }
MV=$($PY -I -c '
import json, sys
from decimal import Decimal, getcontext
getcontext().prec = 40
d = json.load(open(sys.argv[1])); A0, W0 = Decimal(sys.argv[2]), Decimal(sys.argv[3])
mv = [(h["it"], h["mode"], Decimal(h["p_out"][0]) - A0, Decimal(h["p_out"][1]) - W0, max(abs(float(x)) for x in [Decimal(0)] ) ) for h in d["history"]]
big = max(max(abs(a), abs(b)) for _, _, a, b, _ in mv)
print("moves (it mode dA dwf): " + "; ".join("%d %s %+.3e %+.3e" % (i, m, float(a), float(b)) for i, m, a, b, _ in mv) + "; largest %.3e" % float(big))
sys.exit(1 if big > Decimal("1e-8") else 0)' data/A_M_refine_M3_$T.json $A0 $W0); mrc=$?
note "refine moves from zero_mp's values: $MV"
[ $mrc = 0 ] || { echo "$(stamp) STOP: $T refine moved A or wf by more than 1e-8 from zero_mp's values" >> $H; exit 1; }
PO=$($PY -I -c 'import json, sys; print(",".join(json.load(open(sys.argv[1]))["p_out"]))' data/A_M_refine_M3_$T.json)
run A_M_point_M3${T}_stdout certify_M.py point 3 --p=$PO --out=data/A_M_point_M3$T.json --log=logs/A_M_point_M3$T.log; rc=$?
[ $rc = 0 ] || { echo "$(stamp) STOP: $T point run exit $rc: $(tail -3 logs/A_M_point_M3${T}_stdout.log | tr '\n' ' ' | cut -c1-400)" >> $H; exit 1; }
note "point run: $($PY -I -c 'import json, sys; r = json.load(open(sys.argv[1])); print("g_rad %.3e Dg_rad %.3e steps %s sec %.0f" % (r["g_rad"], r["Dg_rad"], r["steps"], r["sec"]))' data/A_M_point_M3$T.json)"
for h in 1e-11 1e-12; do
  for w in 1e-13 1e-12; do
    tag=M3${T}_h${h}_w${w}; box=data/A_M_box_$tag.json
    run A_M_box_${tag}_stdout certify_M.py box 3 --centre=data/A_M_refine_M3_$T.json --use_out --h=$h --w=$w --out=$box --log=logs/A_M_box_$tag.log; rc=$?
    if [ $rc != 0 ]; then note "NOTE: box $tag ended with exit $rc (not repeated): $(tail -3 logs/A_M_box_${tag}_stdout.log | tr '\n' ' ' | cut -c1-300)"; continue; fi
    run A_M_krawczyk_pt_$tag certify_M.py krawczyk --box=$box --point=data/A_M_point_M3$T.json; k=$?
    note "margins $tag exit $k: $(head -1 logs/A_M_krawczyk_pt_$tag.log | cut -c1-200)"
    if [ $k = 0 ]; then
      run A_M_controls_pt_$tag certify_M.py controls --box=$box --point=data/A_M_point_M3$T.json; c=$?
      [ $c = 0 ] || echo "$(stamp) STOP: $T controls $tag exit $c (0 expected)" >> $H
      run A_M_recheck_pt_$tag certify_M_recheck.py $box; r=$?
      note "recheck $tag (no --point option) exit $r"
      run A_M_recheck_pt_${tag}_mutate certify_M_recheck.py $box --mutate; m=$?
      [ $m != 0 ] || echo "$(stamp) STOP: $T recheck --mutate $tag exit 0 (must fail)" >> $H
      echo "$(stamp) PASS: $T box $tag passes the Krawczyk test (controls exit $c, recheck exit $r, recheck --mutate exit $m)" >> $H
    fi
  done
done
note "done"
exit 0
}
