#!/bin/bash
# #1102 lane B: check 2, d18_secant.py scan with --b12=rust and with the default (ell_ddm) at three lambda per state,
# one within 1e-3 of the state's root; code bd424726
{
R=$(cd "$(dirname "$0")/.." && pwd)
SITE=$1; MATTER=$2
cd "$R"
export VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
while read -r stub st D lams kc pin; do
  for b in rust ddm; do
    echo "== $(date -u '+%Y-%m-%d %H:%M') k_c $kc b12 $b" >> scan/scan_kc${kc}_$b.log
    nice -n 10 /Users/nathan/venv-1025dd/bin/python -u "$MATTER/d18_secant.py" scan in/$stub in/$st $D $lams \
      scan/scan_kc${kc}_$b.jsonl --b12=$b --b12_threads=6 --pin=$pin >> scan/scan_kc${kc}_$b.log 2>&1
    echo "exit $? $(date -u '+%Y-%m-%d %H:%M')" >> scan/scan_kc${kc}_$b.log
  done
done <<'LIST'
l1kc55F1025.jsonl sol_l1kc55F1025_D18.125000.npy 18.125 1.77,1.7733,1.78 55 88ccda5c,0fb77df8
l1kc87Ldh370.jsonl sol_l1kc87Ldh370_D21.062500.npy 21.0625 0.89,0.8946,0.9 87 f9a592e5,3fb006df
LIST
exit
}
