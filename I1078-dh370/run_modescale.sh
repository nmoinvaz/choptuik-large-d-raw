#!/bin/bash
# #1078, t5's order (after the pivot ranges): is det M(lam)'s sign at D 3.044375 unresolved because of scale, or because M is near singular? hp/mode_scale.py (main 65ebf0c1, blob 62460d43):
# M(lam) from Solver.mode_matrix, rows and columns equilibrated by powers of two (exact), factored in float64, pivot ratio before and after, scaled sign and ln|det|, mode_det's beside.
# Unit i1078k, 6 threads, nice 10, worktree 1078 at 65ebf0c1 (Python only since the build: no rebuild), the M' 96 state, hmax 0.05 (the #1072 plan). Log: steps_modescale.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_modescale.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 65ebf0c1 ] && [ "$(blob mode_scale.py)" = 62460d43 ] && [ "$(blob $S96)" = 6a0f83d2 ] || { step "STOP: worktree, mode_scale.py or the state not pinned (65ebf0c1, 62460d43, 6a0f83d2)"; exit 1; }
nice -n 10 $PY mode_scale.py selftest > $OUT/modescale_selftest.txt 2>&1; st=$?
step "start; mode_scale.py selftest exit $st (0 wanted): $(tail -1 $OUT/modescale_selftest.txt | cut -c1-260)"
[ $st = 0 ] || { echo "STOP: selftest" > $OUT/STOP_ms.txt; exit 1; }
t0=$(date +%s)
nice -n 10 $PY -u mode_scale.py $OUT/modescale_rows.jsonl $S96 5.14060 5.14066 5.14070 5.140819788786 5.140867320755 --threads=6 > $OUT/modescale.log 2>&1; rc=$?
step "mode_scale.py on 5 lambdas: exit $rc, $(( $(date +%s) - t0 )) s"
t0=$(date +%s)
nice -n 10 $PY -u mode_scale.py $OUT/modescale_noscale.jsonl $S96 5.14066 --threads=6 --mutate=noscale > $OUT/modescale_noscale.log 2>&1; rn=$?
step "control --mutate=noscale at lambda 5.14066: exit $rn, $(( $(date +%s) - t0 )) s"
python3 -I - > $OUT/modescale_summary.txt <<PYEOF
import json
rows = [json.loads(l) for l in open("$OUT/modescale_rows.jsonl")]
for r in rows:
    print(f"lam {r['lam']:.12f}: n {r['n']}; scaled: sign {r['sign']:+.0f} ln|det| {r['ln']:.6f} pivots {r['pmin']:.2e}..{r['pmax']:.2e} ratio {r['ratio']:.2e}; unscaled f64: sign {r['sign_unscaled']:+.0f} ratio {r['ratio_unscaled']:.2e}; kernel mode_det: sign {r['kernel_sign']:+.0f} ln|det| {r['kernel_ln']:.6f} pivots {r['kernel_pmin']:.2e}..{r['kernel_pmax']:.2e}")
for r in (json.loads(l) for l in open("$OUT/modescale_noscale.jsonl")):
    print(f"control noscale at {r['lam']:.12f}: pivot ratio {r['ratio']:.6e} against unscaled {r['ratio_unscaled']:.6e}: {'EQUAL (as required)' if abs(r['ratio'] - r['ratio_unscaled']) <= 1e-12 * r['ratio_unscaled'] else 'DIFFERENT'}")
PYEOF
echo "MODESCALE DONE exit $rc $rn $(stamp) UTC" > $OUT/MODESCALE_DONE.txt
exit 0
}
