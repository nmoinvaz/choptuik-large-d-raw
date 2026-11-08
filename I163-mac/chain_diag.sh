#!/bin/bash
# Issue #163: the diagnostics outside the acceptance, into diag/ (after worker D, in its slot).
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW=/Users/nathan/Source/choptuik-large-d-raw
R="$HERE/run_py.sh"
F145=$RAW/I145-mac/fol
R164=$RAW/I164-mac/roots
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
# the weakest direction by inverse iteration: its planted check, then at D 40.02 and 50.01 on 32x101 and 32x121
$R diag/sigma_planted.log rt_sigma.py --planted
$R diag/sigma_planted_mutate_shift.log rt_sigma.py --planted --mutate=shift
$R diag/sigma_D50_121_norows.log rt_sigma.py "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz"
$R diag/sigma_D50_101.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz
$R diag/sigma_D40_101.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D40.0201_32x101.npz
# where lambda_2 crosses 4 and 5 (the harmonic-0 resonances)
C105=$RAW/I105-mac/cont
C145=$RAW/I145-mac/cont
$R diag/exponents_crossings.log rt_horizon.py exponents $C105/cont_32x101_D21.0000_32x101.npz \
    $C105/cont_32x101_D21.5000_32x101.npz $C105/cont_32x101_D22.0000_32x101.npz $C145/cont_32x101_D33.0000_32x101.npz \
    $C145/cont_32x101_D34.0000_32x101.npz
# Newton again from a landed root, on its own grid (no resampling): does it stay, or jump again?
"$HERE/run_one.sh" diag again_a121_norows "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz" 32x121 0 \
    > "$HERE/diag/again_a121_norows.stdout" 2>&1
"$HERE/run_one.sh" diag again_101 $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz 32x101 0 \
    > "$HERE/diag/again_101.stdout" 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC diag done"
