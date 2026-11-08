#!/bin/bash
# Issue #163: inverse iteration for the weakest direction, and Newton again from landed roots, into diag/
# (after worker C, in its slot).
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW=/Users/nathan/Source/choptuik-large-d-raw
R="$HERE/run_py.sh"
# the weakest direction by inverse iteration: its planted check, then at D 40.02 and 50.01 on 32x101 and 32x121
$R diag/sigma_planted.log rt_sigma.py --planted
$R diag/sigma_planted_mutate_shift.log rt_sigma.py --planted --mutate=shift
$R diag/sigma_D50_121_norows.log rt_sigma.py "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz"
$R diag/sigma_D50_101.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz
$R diag/sigma_D40_101.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D40.0201_32x101.npz
$R diag/sigma_D50_141.log rt_sigma.py $RAW/I145-mac/fol/fol_32x141_D50.0075_32x141.npz
$R diag/sigma_D50_121_rows.log rt_sigma.py "$HERE/acc/a_32x121_D50.0075_32x121.npz"
# Newton again from a landed root, on its own grid (no resampling): does it stay, or jump again?
"$HERE/run_one.sh" diag again_a121_norows "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz" 32x121 0 \
    > "$HERE/diag/again_a121_norows.stdout" 2>&1
"$HERE/run_one.sh" diag again_101 $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz 32x101 0 \
    > "$HERE/diag/again_101.stdout" 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC sigma done"
