#!/bin/bash
# #1078 step 1 (unit i1078b, 6 threads, nice 10): the build's checks on the new hpkernel (c016b932, venv .venv of the 1078 worktree).
# 1c  control: with HP_DENSE_M_MAX unset, lowD_gamma.py on the M' 160 state must refuse in mode_det with an error naming M <= 128 (non-zero exit)
# 1s  selftest: lowD_gamma.py --selftest <uniform D 3.15 M 128 state> <the D 3.044375 L 0.4 M' 128 state> --threads=6, whose lines must equal #1072's step 3d
#     (raw I1072-dh370/selftest_gp_D3.0444_M128.txt, blob 95b6ef1c). Log: steps_step1.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S160=$RAWIN/I1072-dh370/in3/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz
S128M=$RAWIN/I1072-dh370/states3/tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635.npz
S128U=$RAWIN/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
OLD=$RAWIN/I1072-dh370/selftest_gp_D3.0444_M128.txt
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step1.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_$1.txt; step "STOP $1: $2"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = c016b932 ] || stop 1 "worktree not at c016b932"
[ "$(blob $S160)" = 9ccd7a9e ] && [ "$(blob $S128M)" = 218460d9 ] && [ "$(blob $S128U)" = df2ab378 ] && [ "$(blob $OLD)" = 95b6ef1c ] || stop 1 "an input is not its pinned blob (9ccd7a9e, 218460d9, df2ab378, 95b6ef1c)"
step "start; inputs pinned; hpkernel $($PY -c 'import hpkernel; print(hpkernel.isa())'); load $(cut -d' ' -f1-3 /proc/loadavg)"
# 1c: the refusal control
t0=$(date +%s)
env -u HP_DENSE_M_MAX nice -n 10 timeout 7200 $PY -u lowD_gamma.py $OUT/gamma_control_refuse.jsonl $S160 --threads=6 --lam0=5.140802680792423 --xtol=1e-11 > $OUT/control_refuse.log 2>&1; rc=$?
msg=$(grep -E 'dense n x n path is limited to M <= ' $OUT/control_refuse.log | tail -1 | cut -c1-260)
step "1c control (HP_DENSE_M_MAX unset, M' 160 state): exit $rc (non-zero wanted), $(( $(date +%s) - t0 )) s; error: ${msg:-NONE}"
[ $rc != 0 ] && echo "$msg" | grep -q 'M <= 128' && [ ! -s $OUT/gamma_control_refuse.jsonl ] || stop 1c "the control did not refuse as required"
echo "STEP1C PASS $(stamp) UTC" > $OUT/STEP1C_DONE.txt
# 1s: the selftest, lines equal to #1072's
t0=$(date +%s)
nice -n 10 $PY lowD_gamma.py --selftest $S128U $S128M --threads=6 > $OUT/selftest_gp_D3.0444_M128_rebuilt.txt 2>&1; g=$?
if diff -q $OLD $OUT/selftest_gp_D3.0444_M128_rebuilt.txt > /dev/null; then same=EQUAL; else same=DIFFERENT; fi
step "1s selftest on the rebuilt kernel: exit $g (0 wanted), $(( $(date +%s) - t0 )) s; lines against #1072's: $same"
diff $OLD $OUT/selftest_gp_D3.0444_M128_rebuilt.txt > $OUT/selftest_diff_vs_1072.txt 2>&1
[ $g = 0 ] && [ $same = EQUAL ] || stop 1s "the selftest exit $g, lines $same"
echo "STEP1 PASS $(stamp) UTC" > $OUT/STEP1_DONE.txt
exit 0
}
