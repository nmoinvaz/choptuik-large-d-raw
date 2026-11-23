#!/bin/bash
# #1076 macm3b: the check against Theorem A(M=3) certified zero (the coordinator order, hc 2026-11-23 about 13:20 UTC, code 90d914e9):
# zero_mp.py 2.72647588563088 1.01560309485774 CACHE OUT/zero0_cert.jsonl --f3=0.00554371294405835,-0.0722097392350385 --procs=5 --iters=5, from solver/inner_stokes at 90d914e9, 1 thread per BLAS, nice 10.
# Refuses to start when the code is not at 90d914e9 or has local changes in solver, when the cache is not the one the sheet check read, or when the output file exists.
# Records the command, start, end, exit and the cache's sha256 before and after in logs/steps.txt. Own session under caffeinate -is (launch_1070.py).
{
R=/Users/nathan/Source/choptuik-large-d-raw-749p
OUT=$R/I1021-macm3/zero0_cert
CODE=/Users/nathan/Source/choptuik-inner-mp
CODE4=90d914e93307cf199c738d7ac58005094fd44706
IS=$CODE/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
CACHE=$R/I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl
CSHA=8d7cb73287cc733afd332103d2081dab3bd8a4ebdfc88d03b3f0266316d3e331
H=$OUT/logs/steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $CODE rev-parse HEAD)" = "$CODE4" ] && [ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree is not at $CODE4 or has local changes in solver" >> $H; exit 1; }
[ "$(shasum -a 256 $CACHE | cut -c1-64)" = "$CSHA" ] || { echo "$(stamp) STOP: the cache's sha256 is not $CSHA" >> $H; exit 1; }
[ ! -e $OUT/zero0_cert.jsonl ] || { echo "$(stamp) STOP: $OUT/zero0_cert.jsonl exists (the script appends)" >> $H; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "zero0 command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY -u zero_mp.py 2.72647588563088 1.01560309485774 $CACHE $OUT/zero0_cert.jsonl --f3=0.00554371294405835,-0.0722097392350385 --procs=5 --iters=5 > $OUT/logs/zero0_run.log 2>&1" >> $H
echo "zero0 code $(git -C $CODE rev-parse HEAD), solver clean; cache $(wc -l < $CACHE) lines sha256 $CSHA" >> $H
echo "zero0 start $(stamp)" >> $H
(cd $IS && nice -n 10 $PY -u zero_mp.py 2.72647588563088 1.01560309485774 $CACHE $OUT/zero0_cert.jsonl --f3=0.00554371294405835,-0.0722097392350385 --procs=5 --iters=5 > $OUT/logs/zero0_run.log 2>&1); rc=$?
echo "zero0 end $(stamp) exit $rc (0 = located): $(tail -1 $OUT/logs/zero0_run.log | cut -c1-300)" >> $H
echo "zero0 cache after: $(wc -l < $CACHE) lines sha256 $(shasum -a 256 $CACHE | cut -c1-64) (unchanged: $([ "$(shasum -a 256 $CACHE | cut -c1-64)" = "$CSHA" ] && echo yes || echo NO))" >> $H
echo "zero0 done $(stamp)" >> $H
exit 0
}
