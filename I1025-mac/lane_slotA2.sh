#!/bin/bash
{
# #1025 T2 (u0resolve_criteria.log, T2 addendum): the Ks 45 re-solve at u0 0.04 from Fb, k_c 55, D 16, then the hybrid scan on its state.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
L=2.15,2.20,2.22,2.24,2.26,2.28,2.33
cd $M
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') ell_refine.py l1kc55Fb1025 55 l1kc55Fk1025 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.04 --Ks 45 --tol 1e-12 --wait 60"
timeout 14400 nice -n 10 /Users/nathan/venv-314/bin/python -u ell_refine.py l1kc55Fb1025 55 l1kc55Fk1025 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.04 --Ks 45 --tol 1e-12 --wait 60 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve'
echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
cat data/l1kc55Fk1025.jsonl
if [ -f data/sol_l1kc55Fk1025_D16.0000.npy ] && /Users/nathan/venv-314/bin/python -c "import json,sys; r=[json.loads(l) for l in open('data/l1kc55Fk1025.jsonl')][-1]; sys.exit(0 if r['F'] < 1e-8 else 1)"; then
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') p1d_scan.py data/l1kc55Fk1025.jsonl data/sol_l1kc55Fk1025_D16.0000.npy 16 $L"
  RAYON_NUM_THREADS=4 timeout 10800 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/p1d_scan.py $M/data/l1kc55Fk1025.jsonl $M/data/sol_l1kc55Fk1025_D16.0000.npy 16 $L < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve'
  echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
else
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') no state or F >= 1e-8: no scan (T2 addendum)"
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane slotA2 (T2) done"
exit
}
