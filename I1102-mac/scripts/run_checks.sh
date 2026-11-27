#!/bin/bash
# #1102 lane A: check 1 (ellrs's block 12 against DDEll's, bit for bit), its controls and the timing; code bd424726
{
R=$(cd "$(dirname "$0")/.." && pwd)
SITE=$1; MATTER=$2
cd "$R"
export VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
while read -r stub st D lams kc; do
  echo "== $(date -u '+%Y-%m-%d %H:%M') k_c $kc" >> checks/check_kc$kc.log
  nice -n 10 /Users/nathan/venv-1025dd/bin/python -u "$MATTER/ell_b12rs.py" check in/$stub in/$st $D $lams --threads=6,1 \
    --controls=1 --out=checks/check.jsonl >> checks/check_kc$kc.log 2>&1
  echo "exit $? $(date -u '+%Y-%m-%d %H:%M')" >> checks/check_kc$kc.log
done <<'LIST'
l1kc31r1025.jsonl sol_l1kc31r1025_D10.5000.npy 10.5 2.87 31
l1kc55F1025.jsonl sol_l1kc55F1025_D18.125000.npy 18.125 1.775 55
l1kc87Ldh370.jsonl sol_l1kc87Ldh370_D21.062500.npy 21.0625 0.895 87
LIST
exit
}
