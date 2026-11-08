#!/bin/bash
# Issue #163: the verdicts of the criteria in README.md, into fit/ (rt_grids.py and rt_roots.py).
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW=/Users/nathan/Source/choptuik-large-d-raw
R="$HERE/run_py.sh"
D50=50.007491
D60=60.001952
for G in 32x121 32x123; do
    # criterion 1: with the rows; criterion 2: without them (the control); and the planted shift of rt_grids
    $R fit/acc_${G}.log rt_grids.py "$HERE/acc/a_${G}.jsonl" "$HERE/acc/b_${G}.jsonl" --D $D50 --tol 1e-14 --tol_ab 1e-18
    $R fit/acc_${G}_norows.log rt_grids.py "$HERE/acc/a_${G}_mutnorows.jsonl" "$HERE/acc/b_${G}_mutnorows.jsonl" \
        --D $D50 --tol 1e-12
    $R fit/acc_${G}_norows_tol14.log rt_grids.py "$HERE/acc/a_${G}_mutnorows.jsonl" "$HERE/acc/b_${G}_mutnorows.jsonl" \
        --D $D50 --tol 1e-14 --tol_ab 1e-18
    $R fit/roots_acc_${G}.log rt_roots.py "$HERE/acc/a_${G}_D50.0075_${G}.npz" "$HERE/acc/b_${G}_D50.0075_${G}.npz"
    $R fit/roots_acc_${G}_norows.log rt_roots.py "$HERE/acc/a_${G}_mutnorows_D50.0075_${G}.npz" \
        "$HERE/acc/b_${G}_mutnorows_D50.0075_${G}.npz"
done
for N in 93 95 97 99; do
    G=32x$N
    # criterion 4: with the rows, and #164's pair without them
    $R fit/pair_${G}.log rt_roots.py "$HERE/pair/a_${G}_D60.0020_${G}.npz" "$HERE/pair/b_${G}_D60.0020_${G}.npz"
    $R fit/pair_${G}_norows.log rt_roots.py "$RAW/I164-mac/roots/a101_${G}_D60.0020_${G}.npz" \
        "$RAW/I164-mac/roots/b121_${G}_D60.0020_${G}.npz"
    $R fit/pair_grids_${G}.log rt_grids.py "$HERE/pair/a_${G}.jsonl" "$HERE/pair/b_${G}.jsonl" --D $D60 --tol 1e-12
done
# the controls of the checks themselves: rt_grids' planted shift and rt_roots' planted pair and identity
$R fit/acc_32x121_mutate_shift.log rt_grids.py "$HERE/acc/a_32x121.jsonl" "$HERE/acc/b_32x121.jsonl" --D $D50 \
    --tol 1e-14 --tol_ab 1e-18 --mutate=shift
$R fit/roots_acc_32x121_mutate_same.log rt_roots.py "$HERE/acc/a_32x121_D50.0075_32x121.npz" \
    "$HERE/acc/b_32x121_D50.0075_32x121.npz" --mutate=same
$R fit/roots_acc_32x121_mutate_mid.log rt_roots.py "$HERE/acc/a_32x121_D50.0075_32x121.npz" \
    "$HERE/acc/b_32x121_D50.0075_32x121.npz" --mutate=mid
