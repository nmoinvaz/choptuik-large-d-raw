#!/bin/bash
# #1076 macm3b: the coordinator's follow-up order (hc 2026-11-23 about 13:25 UTC): after zero_mp (zero0.sh) ends, one point at its final location:
# value_mp.py point <A_final> <wf_final> 0.00554371294405835 -0.0722097392350385 (the last row of zero0_cert.jsonl, its floats as repr), 1 process, nice 10, 1 thread per BLAS.
# Waits for the line "zero0 done" in logs/steps.txt (zero0.sh's last line); stops on a STOP line, a missing row or code not at 90d914e9. Records in logs/steps_point.txt. Own session under caffeinate -is.
{
R=/Users/nathan/Source/choptuik-large-d-raw-749p
OUT=$R/I1021-macm3/zero0_cert
CODE=/Users/nathan/Source/choptuik-inner-mp
CODE5=90d914e93307cf199c738d7ac58005094fd44706
IS=$CODE/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
H=$OUT/logs/steps.txt
HP=$OUT/logs/steps_point.txt
stamp() { date -u '+%F %T'; }
echo "zero0_point waiting for zero0 done $(stamp)" >> $HP
while ! grep -q '^zero0 done' $H; do
  if grep -q 'STOP:' $H; then echo "$(stamp) STOP: a STOP line in $H" >> $HP; exit 1; fi
  sleep 30
done
echo "zero0_point: zero_mp's wrapper is done $(stamp): $(grep '^zero0 end' $H | cut -c1-300)" >> $HP
[ "$(git -C $CODE rev-parse HEAD)" = "$CODE5" ] && [ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree is not at $CODE5 or has local changes in solver" >> $HP; exit 1; }
[ -s $OUT/zero0_cert.jsonl ] || { echo "$(stamp) STOP: no rows in $OUT/zero0_cert.jsonl" >> $HP; exit 1; }
AW=$($PY -c 'import json, sys; r = [json.loads(l) for l in open(sys.argv[1])][-1]; print(repr(r["A"]), repr(r["wf"]), r["it"])' $OUT/zero0_cert.jsonl) || { echo "$(stamp) STOP: could not read the last row" >> $HP; exit 1; }
set -- $AW; A=$1; WF=$2; IT=$3
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "zero0_point final location: the last row (iteration $IT) A $A wf $WF" >> $HP
echo "zero0_point command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY -u value_mp.py point $A $WF 0.00554371294405835 -0.0722097392350385 > $OUT/zero0_point.json 2> $OUT/logs/zero0_point.err" >> $HP
echo "zero0_point start $(stamp)" >> $HP
(cd $IS && nice -n 10 $PY -u value_mp.py point $A $WF 0.00554371294405835 -0.0722097392350385 > $OUT/zero0_point.json 2> $OUT/logs/zero0_point.err); rc=$?
echo "zero0_point end $(stamp) exit $rc: $(cut -c1-300 $OUT/zero0_point.json)" >> $HP
echo "zero0_point done $(stamp)" >> $HP
exit 0
}
