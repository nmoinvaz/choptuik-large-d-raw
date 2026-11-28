#!/bin/bash
# #1109 stage 1c2: A (ell_fastdd check) and B (d18_secant root with --b12=rust) at once on R0; logs in c2/. nice 10, timeout 14400 each.
{
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
W=$HOME/Source/choptuik-ellrs/solver/matter
PY=$HOME/venv-314/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=2
REC=$H/c/in/l1kc127k070w2.jsonl; ST=$H/c/in/sol_l1kc127k070w2_D23.0000.npy
cd $W || exit 1
L=$H/c2/run_c2.log
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
( t0=$(date +%s); nice -n 10 timeout 14400 $PY -u ell_fastdd.py check $REC $ST 23.0 0.0458 --hybrid=1 > $H/c2/fastdd_check_r0.log 2>&1; echo "A exit $? $(( $(date +%s) - t0 )) s $(date -u +%H:%M:%S)" >> $L ) &
pa=$!
( t0=$(date +%s); nice -n 10 timeout 14400 $PY -u d18_secant.py run $REC $ST 23.0 0.0440 0.0470 $H/c2/root_r0_rust.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2 --pin=90d3e655,d1a3a641 > $H/c2/root_r0_rust.log 2>&1; echo "B exit $? $(( $(date +%s) - t0 )) s $(date -u +%H:%M:%S)" >> $L ) &
pb=$!
echo "pids A $pa B $pb" >> $L
wait $pa $pb
echo "done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
exit
}
