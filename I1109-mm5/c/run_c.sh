#!/bin/bash
# #1109 stage 1c (R0, k_c 127, D 23.0): jac, svd, report, valley, then three d18_secant.py roots at once. 2 threads per process,
# nice 10. Stops at bar 1 (jac not the record system); stops the two roots when the control misses bar 2.
{
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
C=$H/c
W=$HOME/Source/choptuik-1109/solver/matter
PY=$HOME/venv-314/bin/python
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
REC=$C/in/l1kc127k070w2.jsonl; ST=$C/in/sol_l1kc127k070w2_D23.0000.npy
D=23.0
cd $W || exit 1
L=$C/run_c.log
t0=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
nice -n 10 timeout 7200 $PY i1101_weakdir.py jac $REC $ST $D $C/jac_r0.npz --pin=90d3e655,d1a3a641 > $C/jac_r0.log 2>&1
rc=$?; echo "jac rc $rc $(( $(date +%s) - t0 )) s" >> $L
if [ $rc != 0 ] || ! grep -q "the record system" $C/jac_r0.log; then echo "STOP bar 1: jac printed not the record system (rc $rc): $(head -n 2 $C/jac_r0.log | cut -c1-200 | tr '\n' ' ')" >> $L; exit 3; fi
nice -n 10 timeout 3600 $PY i1101_weakdir.py svd $C/jac_r0.npz $C/svd_r0.npz > $C/svd_r0.log 2>&1
echo "svd rc $? $(( $(date +%s) - t0 )) s" >> $L
nice -n 10 timeout 3600 $PY i1101_weakdir.py report $C/jac_r0.npz $C/svd_r0.npz $D r0=$REC:$ST --out=$C/rep_r0.json > $C/report_r0.log 2>&1
echo "report rc $? $(( $(date +%s) - t0 )) s" >> $L
nice -n 10 timeout 7200 $PY i1101_weakdir.py valley $C/jac_r0.npz $C/svd_r0.npz $REC $ST $D --ts=1e-3,1e-2,1e-1 --save=1e-2:$C/sol_w01_D23.0000.npy,1e-1:$C/sol_w10_D23.0000.npy --refreeze=1 > $C/valley_r0.log 2>&1
echo "valley rc $? $(( $(date +%s) - t0 )) s" >> $L
if [ ! -f $C/sol_w01_D23.0000.npy ] || [ ! -f $C/sol_w10_D23.0000.npy ]; then echo "STOP: valley did not save both states" >> $L; exit 4; fi
# widened bracket on a refusal (exit 2): the half-width doubled about the centre, appended to the same output
root() {  # NAME STUB STATE LO HI LO2 HI2 [extra args]
  name=$1; stub=$2; st=$3; lo=$4; hi=$5; lo2=$6; hi2=$7; shift 7
  t1=$(date +%s)
  nice -n 10 timeout 14400 $PY d18_secant.py run $stub $st $D $lo $hi $C/root_$name.jsonl --tol=1e-6 --maxev=20 --b12=fast "$@" >> $C/root_$name.log 2>&1
  rc=$?; echo "root $name bracket ($lo, $hi) rc $rc $(( $(date +%s) - t1 )) s" >> $L
  if [ $rc = 2 ]; then
    echo "root $name: refused, widening to ($lo2, $hi2)" >> $L
    echo "== widened bracket ($lo2, $hi2) after the refusal" >> $C/root_$name.log
    nice -n 10 timeout 14400 $PY d18_secant.py run $stub $st $D $lo2 $hi2 $C/root_$name.jsonl --tol=1e-6 --maxev=20 --b12=fast "$@" >> $C/root_$name.log 2>&1
    rc=$?; echo "root $name widened ($lo2, $hi2) rc $rc $(( $(date +%s) - t1 )) s" >> $L
  fi
  return $rc
}
root r0 $REC $ST 0.0 0.1 -0.05 0.15 --pin=90d3e655,d1a3a641 &
p0=$!; echo $p0 > $C/root_r0.pid
root w01 $C/sol_w01_D23.0000.jsonl $C/sol_w01_D23.0000.npy -0.1 0.2 -0.25 0.35 &
p1=$!; echo $p1 > $C/root_w01.pid
root w10 $C/sol_w10_D23.0000.jsonl $C/sol_w10_D23.0000.npy -0.3 0.4 -0.65 0.75 &
p2=$!; echo $p2 > $C/root_w10.pid
echo "roots started $(date -u '+%H:%M:%S UTC'): pids $p0 $p1 $p2" >> $L
wait $p0; echo "control finished rc $? $(date -u '+%H:%M:%S UTC')" >> $L
ok=$($PY -I - <<PYEOF
import json
r=[json.loads(l) for l in open("$C/root_r0.jsonl") if l.strip()]
f=[x for x in r if x.get("kind")=="root"]
print("ok" if f and abs(f[-1]["lam_lin"]-0.045967998)<=1e-5 else "fail")
PYEOF
)
echo "bar 2 (control within 1e-5 of 0.045967998): $ok" >> $L
if [ "$ok" != "ok" ]; then
  echo "STOP bar 2: stopping the other two roots (pgid kill of their pythons)" >> $L
  pkill -TERM -f "d18_secant.py run $C/sol_w" ; kill $p1 $p2 2>/dev/null
fi
wait $p1; echo "w01 finished rc $?" >> $L
wait $p2; echo "w10 finished rc $?" >> $L
echo "done $(date -u '+%Y-%m-%d %H:%M:%S UTC') total $(( $(date +%s) - t0 )) s" >> $L
exit
}
