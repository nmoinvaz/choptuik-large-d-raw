#!/bin/bash
# #1109 stage 1c2 check: this machine's hybrid at dh170's two lambdas (0.045, 0.05) on R0, --b12=rust, d18_secant scan.
{
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
cd $HOME/Source/choptuik-ellrs/solver/matter || exit 1
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=2
REC=$H/c/in/l1kc127k070w2.jsonl; ST=$H/c/in/sol_l1kc127k070w2_D23.0000.npy
t0=$(date +%s); echo "scan start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $H/c2/run_scan.log
nice -n 10 timeout 14400 $HOME/venv-314/bin/python -u d18_secant.py scan $REC $ST 23.0 0.045,0.05 $H/c2/scan_r0_rust.jsonl --b12=rust --b12_threads=2 --pin=90d3e655,d1a3a641 > $H/c2/scan_r0_rust.log 2>&1
echo "scan exit $? $(( $(date -u +%s) - t0 )) s $(date -u +%H:%M:%S)" >> $H/c2/run_scan.log
exit
}
