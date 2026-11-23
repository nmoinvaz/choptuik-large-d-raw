#!/bin/bash
# #1079 macm3b step 2 (refine): p = (A, wf, B3 = -2 Im F3, C3 = 2 Re F3) from step 1's rows, then certify_M.py refine 3 --p=<p> --iters=3 --tag=x1 and x2 in parallel (2 processes),
# from main's solver/proof (worktree ~/Source/choptuik-large-d-1079 at a4cd5eaa), nice 10, 1 thread per BLAS. Stops (STOP line) when a step-1 row is not valued, and after the refinements
# when A or wf moved by more than 1e-8 from the zero_mp values. Records in $P/steps.txt. Own session under caffeinate -is (launch_1070.py).
{
P=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3
W=/Users/nathan/Source/choptuik-large-d-1079
MAIN=a4cd5eaa7b297ffc6f171551fa15ba054e970e21
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$P/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $W rev-parse HEAD)" = "$MAIN" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { echo "$(stamp) STOP: the main worktree is not at $MAIN or has tracked changes" >> $H; exit 1; }
# step 1's rows -> p
mkp() {   # mkp ROW.json A WF -> prints "A,WF,B3,C3" (B3 and C3 as repr of the doubled floats) or fails when the row is not valued
    $PY -I -c '
import json, sys
r = json.load(open(sys.argv[1]))
assert r["valued"] and r["info"] < 1e-8 and r["ymax"] <= 100, "row not valued: " + str({k: r[k] for k in ("valued", "info", "ymax")})
print("%s,%s,%r,%r" % (sys.argv[2], sys.argv[3], -2 * r["F3im"], 2 * r["F3re"]))' "$1" "$2" "$3"
}
P1=$(mkp $P/point_x1.json 3.446218246366727 0.347606965217407) || { echo "$(stamp) STOP: step 1's row for x1 is not valued or missing" >> $H; exit 1; }
P2=$(mkp $P/point_x2.json 3.526473056695715 0.211497981391215) || { echo "$(stamp) STOP: step 1's row for x2 is not valued or missing" >> $H; exit 1; }
echo "refine p x1 = $P1" >> $H
echo "refine p x2 = $P2" >> $H
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/solver/proof || exit 1
echo "refine x1 command: cd $W/solver/proof && nice -n 10 $PY certify_M.py refine 3 --p=$P1 --iters=3 --tag=x1 > logs/A_M_refine_M3_x1_stdout.log 2>&1" >> $H
echo "refine x2 command: cd $W/solver/proof && nice -n 10 $PY certify_M.py refine 3 --p=$P2 --iters=3 --tag=x2 > logs/A_M_refine_M3_x2_stdout.log 2>&1" >> $H
echo "refine start $(stamp)" >> $H
(nice -n 10 $PY certify_M.py refine 3 --p=$P1 --iters=3 --tag=x1 > logs/A_M_refine_M3_x1_stdout.log 2>&1; echo "refine x1 end $(stamp) exit $?" >> $H) &
(nice -n 10 $PY certify_M.py refine 3 --p=$P2 --iters=3 --tag=x2 > logs/A_M_refine_M3_x2_stdout.log 2>&1; echo "refine x2 end $(stamp) exit $?" >> $H) &
wait
# moves of A and wf from the zero_mp values
for t in x1 x2; do
  if [ $t = x1 ]; then A0=3.446218246366727; W0=0.347606965217407; else A0=3.526473056695715; W0=0.211497981391215; fi
  $PY -I -c '
import json, sys
from decimal import Decimal, getcontext
getcontext().prec = 40
d = json.load(open(sys.argv[1])); A0, W0 = Decimal(sys.argv[2]), Decimal(sys.argv[3])
mv = []
for h in d["history"]:
    a, w = Decimal(h["p_out"][0]), Decimal(h["p_out"][1])
    mv.append((h["it"], h["mode"], a - A0, w - W0))
print("moves from the zero_mp values per iteration (it, mode, dA, dwf): " + "; ".join("%d %s %+.3e %+.3e" % (i, m, float(x), float(y)) for i, m, x, y in mv))
big = max(max(abs(x), abs(y)) for _, _, x, y in mv)
print("largest move %.3e" % float(big))
sys.exit(1 if big > Decimal("1e-8") else 0)' $W/solver/proof/data/A_M_refine_M3_$t.json $A0 $W0 > $P/refine_moves_$t.txt 2>&1; rc=$?
  echo "refine $t moves (exit $rc, 0 = within 1e-8): $(cat $P/refine_moves_$t.txt | tr '\n' ' ' | cut -c1-400)" >> $H
  [ $rc = 0 ] || echo "$(stamp) STOP: refine $t moved A or wf by more than 1e-8 from the zero_mp values (or its json is missing)" >> $H
done
echo "refine done $(stamp)" >> $H
exit 0
}
