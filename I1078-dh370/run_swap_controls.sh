#!/bin/bash
# #1078 (t5's hc: stop the identity control after 3 steps, or rerun it on b6d0f587 with --ntol 1e-27): waits for run_layout_swap.sh's mode_scale step to end (SWAP_STEP_MODESCALE_DONE.txt),
# stops that chain (unit i1078u) before its identity control gets anywhere (its 12-step polish would sit at the 3e-29 floor), and runs the tool's two controls with layout_swap.py of main b6d0f587
# (worktree ~/Source/choptuik-large-d-1078n; --ntol default 1e-27): the identity move (--like IN: |F| at IN's level, Delta unchanged, exit 0) and --polish 0 on the real move (exit 1). Unit i1078v, 4 threads, nice 10.
# Log: steps_swap_controls.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WTK=/home/nathan/Source/choptuik-large-d-1078      # the kernel's venv (c016b932 build)
WTN=/home/nathan/Source/choptuik-large-d-1078n     # main b6d0f587
PY=$WTK/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
S315=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_swap_controls.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WTN/hp || exit 9
[ "$(git -C $WTN rev-parse --short=8 HEAD)" = b6d0f587 ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $S315)" = 9e683a14 ] || { step "STOP: worktree or a state not pinned"; echo "CONTROLS NOT RUN $(stamp) UTC" > $OUT/SWAP_CONTROLS_DONE.txt; exit 1; }
step "waiting for SWAP_STEP_MODESCALE_DONE.txt (the chain i1078u); layout_swap.py blob $(blob layout_swap.py)"
while [ ! -f $OUT/SWAP_STEP_MODESCALE_DONE.txt ] && [ "$(systemctl --user is-active i1078u)" = active ]; do sleep 10; done
if [ "$(systemctl --user is-active i1078u)" = active ]; then systemctl --user stop i1078u; step "stopped unit i1078u after its mode_scale step ($(cat $OUT/SWAP_STEP_MODESCALE_DONE.txt)); its identity control is replaced by this unit's"; else step "unit i1078u had ended on its own ($(cat $OUT/SWAP_DONE.txt 2>/dev/null))"; fi
rm -f $OUT/layout_swap_control_identity.npz $OUT/layout_swap_control_identity.log $OUT/layout_swap_control_polish0.npz $OUT/layout_swap_control_polish0.log
t0=$(date +%s)
nice -n 10 $PY -u layout_swap.py $S315 $OUT/layout_swap_control_identity.npz --like $S315 --polish 12 --threads 4 > $OUT/layout_swap_control_identity.log 2>&1; ri=$?
step "control (identity, --like IN, polish 12, ntol 1e-27): exit $ri (0 wanted), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/layout_swap_control_identity.log | cut -c1-300)"
t0=$(date +%s)
nice -n 10 $PY -u layout_swap.py $S315 $OUT/layout_swap_control_polish0.npz --like $S96 --polish 0 --threads 4 > $OUT/layout_swap_control_polish0.log 2>&1; rp=$?
step "control (real move, --polish 0): exit $rp (1 wanted), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/layout_swap_control_polish0.log | cut -c1-300)"
echo "SWAP CONTROLS DONE: identity exit $ri, polish0 exit $rp $(stamp) UTC" > $OUT/SWAP_CONTROLS_DONE.txt
exit 0
}
