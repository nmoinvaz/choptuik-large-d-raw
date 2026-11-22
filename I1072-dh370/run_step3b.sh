#!/bin/bash
# #1072 step 3, continued after 3c's stop (unit i1072f, 6 threads, nice 10, worktree 1072b at ae96bcc6): 3c (L 0.4 at M' 96) did not converge in it1 = 4 calls
# (|F| 2.09e-3, 1.27e-5, 4.57e-7, 4.98e-9); t5's order stops only if the M' 128 solve fails, so the gp selftest and gamma on the converged M' 128 state go on.
# 3d  gp selftest: lowD_gamma.py --selftest <uniform D 3.15 M 128 state> <the D 3.044375 L 0.4 M' 128 state> (exit 0)
# 3e  gamma at M' 128: --lam0=5.1408197887863025 (lam_guess at the state's D 3.044375) --xtol=1e-11. Log: steps_step3b.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
S128U=/home/nathan/Source/choptuik-large-d-raw-push960/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
WT=/home/nathan/Source/choptuik-large-d-1072b
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
J=$OUT/solve_step3.jsonl; G=$OUT/gamma_D3.0444.jsonl; LAM0=5.1408197887863025
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step3b.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_3b$1.txt; step "STOP $1: $2"; exit 1; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = ae96bcc6 ] || stop d "worktree not at ae96bcc6"
P128=$(jq -r 'select(.converged==true and .L==0.4 and .Mp==128) | .saved' $J | tail -1); [ -f "$P128" ] || stop d "no saved L 0.4 M' 128 state"
step "start; the M' 128 state $(basename $P128 | cut -c1-90); lam0 $LAM0; load $(cut -d' ' -f1-3 /proc/loadavg)"
nice -n 10 $PY lowD_gamma.py --selftest $S128U $P128 --threads=6 > $OUT/selftest_gp_D3.0444_M128.txt 2>&1; g=$?
step "3d: lowD_gamma.py --selftest <uniform D 3.15 M 128> <D 3.044375 L 0.4 M' 128>: exit $g (0 wanted); $(tail -2 $OUT/selftest_gp_D3.0444_M128.txt | cut -c1-230 | tr '\n' '|')"
[ $g = 0 ] || stop d "the gp selftest exited $g"
echo "STEP3D PASS $(stamp) UTC" > $OUT/STEP3D_DONE.txt
t0=$(date +%s)
nice -n 10 timeout 21600 $PY -u lowD_gamma.py $G $P128 --threads=6 --lam0=$LAM0 --xtol=1e-11 > $OUT/gamma_D3.0444_M128.log 2>&1; rc=$?
step "3e gamma M' 128: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G | jq -c '{M,gamma,lam,F,n_signchanges,n_det,seconds}' | cut -c1-230)"
[ $rc = 0 ] || stop e "gamma at M' 128 exited $rc"
echo "STEP3E_M128 DONE $(stamp) UTC" > $OUT/STEP3E_M128_DONE.txt
exit 0
}
