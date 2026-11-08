#!/bin/bash
# Issue #163: the bound on the smallest gain with rough right-hand sides (rt_sigma.py --rough, code 0149965), after
# chain_sigma2.sh: is the weak direction's left vector rough on the grid (a polynomial copy of a horizon branch) or
# smooth (a weak direction of the equations)?
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW=/Users/nathan/Source/choptuik-large-d-raw
R="$HERE/run_py.sh"
# (run at once in the free slot of worker D)
$R diag/sigma3_D50_101_rough.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz --rough --starts 2
$R diag/sigma3_D50_121_norows_rough.log rt_sigma.py "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz" --rough \
    --starts 2
$R diag/sigma3_D40_101_rough.log rt_sigma.py $RAW/I145-mac/cont/cont_32x101_D40.0201_32x101.npz --rough --starts 2
$R diag/sigma3_D50_141_rough.log rt_sigma.py $RAW/I145-mac/fol/fol_32x141_D50.0075_32x141.npz --rough --starts 2
$R diag/sigma3_D50_121_rows_rough.log rt_sigma.py "$HERE/acc/a_32x121_D50.0075_32x121.npz" --rough --starts 2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC sigma3 done"
