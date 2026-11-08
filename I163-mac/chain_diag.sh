#!/bin/bash
# Issue #163: the diagnostics outside the acceptance, into diag/ (after worker D, in its slot).
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW=/Users/nathan/Source/choptuik-large-d-raw
R="$HERE/run_py.sh"
F145=$RAW/I145-mac/fol
R164=$RAW/I164-mac/roots
# how fast the branches' Chebyshev coefficients fall (lambda_2 and lambda_4 at D 50.01, k = 0 and 1/2)
$R diag/branch_cheb.log rt_branch_cheb.py --lam 5.68,26.23,26.23 --om 0,0,3.87
$R diag/branch_cheb_planted.log rt_branch_cheb.py --lam 5.68,26.23 --om 0,0 --planted
# J along #145's 32x121 pair at D 50.01 and #164's 32x97 pair at D 60.00 on finer grids, and their content
$R diag/pairfine_D50_121.log rt_pair_fine.py $F145/fol_32x121_D50.0075_32x121.npz \
    $F145/from141_32x121_D50.0075_32x121.npz 121,141,181
$R diag/pairfine_D50_121_mutate_f64.log rt_pair_fine.py $F145/fol_32x121_D50.0075_32x121.npz \
    $F145/from141_32x121_D50.0075_32x121.npz 121,141 --mutate=f64
$R diag/pairfine_D60_97.log rt_pair_fine.py $R164/a101_32x97_D60.0020_32x97.npz $R164/b121_32x97_D60.0020_32x97.npz \
    97,141,181
# the same for this task's pairs with the rows
$R diag/pairfine_D50_121_rows.log rt_pair_fine.py "$HERE/acc/a_32x121_D50.0075_32x121.npz" \
    "$HERE/acc/b_32x121_D50.0075_32x121.npz" 121,141
$R diag/pairfine_D50_121_norows.log rt_pair_fine.py "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz" \
    "$HERE/acc/b_32x121_mutnorows_D50.0075_32x121.npz" 121,141
# is the 32x101 root exact in xi at D 60 as well
$R diag/resres_cont101_D60.log rt_resample_res.py $RAW/I145-mac/cont/cont_32x101_D60.0020_32x101.npz 101,121,141
$R diag/resres_mutate_perturb.log rt_resample_res.py $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz 101,121 \
    --mutate=perturb
# where lambda_2 crosses 4 and 5 (the harmonic-0 resonances)
C105=$RAW/I105-mac/cont
C145=$RAW/I145-mac/cont
$R diag/exponents_crossings.log rt_horizon.py exponents $C105/cont_32x101_D21.0000_32x101.npz \
    $C105/cont_32x101_D21.5000_32x101.npz $C105/cont_32x101_D22.0000_32x101.npz $C145/cont_32x101_D33.0000_32x101.npz \
    $C145/cont_32x101_D34.0000_32x101.npz
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC diag done"
until grep -q "queue .* done" "$HERE/pair/worker_C.stdout" 2>/dev/null; do sleep 15; done
"$HERE/run_verdicts.sh"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC verdicts done"
