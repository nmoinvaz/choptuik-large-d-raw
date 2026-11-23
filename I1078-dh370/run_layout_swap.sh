#!/bin/bash
# #1078, t5's order (comment of 22:20 UTC, run 2; unit i1078u): hp/layout_swap.py (main 3279c81f) moves the D 3.15 M' 96 state (9e683a14: 17 nodes to x 0.9, map s0 1.8326 L 0.7) to the layout of the
# D 3.044375 M' 96 state (6a0f83d2: 21 nodes to x 0.975, map s0 1.9635 L 0.4) and re-converges it (--polish 12, 4 threads); then mode_scale.py --small=200 on the result at lambda 4.397684106690
# (its row has the kernel's mode_det of the swapped state; the D 3.15 layout's is in modescale_small200_d315.jsonl); then the tool's own controls on this machine: the identity move (--like IN)
# and --polish 0 on the real move (exit 1). Stops after a failed step (STOP_SWAP_<step>.txt); a failed polish (exit 1) stops before mode_scale. nice 10. Log: steps_swap.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
S315=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
SW=$OUT/layout_swap_D3.15_to_D3.0444layout_M96.npz
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_swap.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_SWAP_$1.txt; step "STOP $1: $2"; echo "SWAP CHAIN STOPPED at $1 $(stamp) UTC" > $OUT/SWAP_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 3279c81f ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $S315)" = 9e683a14 ] && [ "$(blob mode_scale.py)" = 794be9b9 ] || stop 0 "worktree, a state or mode_scale.py not pinned (3279c81f, 6a0f83d2, 9e683a14, 794be9b9)"
step "start; layout_swap.py blob $(blob layout_swap.py); hpkernel $($PY -c 'import hpkernel; print(hpkernel.isa())' 2>/dev/null); load $(cut -d' ' -f1-3 /proc/loadavg)"
# the swap
t0=$(date +%s)
nice -n 10 $PY -u layout_swap.py $S315 $SW --like $S96 --polish 12 --threads 4 > $OUT/layout_swap_D3.15_to_D3.0444layout.log 2>&1; rc=$?
step "layout_swap D 3.15 -> D 3.044375 layout: exit $rc (0 = converged to 1e-20), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/layout_swap_D3.15_to_D3.0444layout.log | cut -c1-300)"
echo "SWAP STEP LAYOUT_SWAP rc $rc $(stamp) UTC" > $OUT/SWAP_STEP_LAYOUT_DONE.txt
[ $rc = 0 ] || stop layout_swap "the swap did not converge (exit $rc): no mode_scale on it"
# mode_scale on the swapped state
t0=$(date +%s)
nice -n 10 $PY -u mode_scale.py $OUT/modescale_small200_swap.jsonl $SW 4.397684106690 --hmax=0.05 --threads=4 --small=200 > $OUT/modescale_small200_swap.log 2>&1; rc=$?
step "mode_scale --small=200 on the swapped state at lambda 4.397684106690: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/modescale_small200_swap.log | cut -c1-300)"
echo "SWAP STEP MODESCALE rc $rc $(stamp) UTC" > $OUT/SWAP_STEP_MODESCALE_DONE.txt
[ $rc = 0 ] || stop modescale "mode_scale exit $rc"
# the tool's own controls
t0=$(date +%s)
nice -n 10 $PY -u layout_swap.py $S315 $OUT/layout_swap_control_identity.npz --like $S315 --polish 12 --threads 4 > $OUT/layout_swap_control_identity.log 2>&1; ri=$?
step "control (identity, --like IN, polish 12): exit $ri (0 wanted), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/layout_swap_control_identity.log | cut -c1-300)"
t0=$(date +%s)
nice -n 10 $PY -u layout_swap.py $S315 $OUT/layout_swap_control_polish0.npz --like $S96 --polish 0 --threads 4 > $OUT/layout_swap_control_polish0.log 2>&1; rp=$?
step "control (real move, --polish 0): exit $rp (1 wanted), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/layout_swap_control_polish0.log | cut -c1-300)"
echo "SWAP CHAIN DONE controls: identity exit $ri, polish0 exit $rp $(stamp) UTC" > $OUT/SWAP_DONE.txt
exit 0
}
