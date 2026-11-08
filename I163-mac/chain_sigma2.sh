#!/bin/bash
# Issue #163: rt_sigma.py's planted check and its control at the bound version (code 3ad3771), and the D 50 32x121 root
# again with it, after chain_sigma.sh (whose first three ran the earlier inverse-iteration version).
HERE="$(cd "$(dirname "$0")" && pwd)"
R="$HERE/run_py.sh"
until grep -q "sigma done" "$HERE/diag/chain_sigma.stdout" 2>/dev/null; do sleep 15; done
$R diag/sigma2_planted.log rt_sigma.py --planted
$R diag/sigma2_planted_mutate_shift.log rt_sigma.py --planted --mutate=shift
$R diag/sigma2_D50_121_norows.log rt_sigma.py "$HERE/acc/a_32x121_mutnorows_D50.0075_32x121.npz"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC sigma2 done"
