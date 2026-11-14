#!/bin/bash
# I377 queue 7: the collocation (css_scan.py, N = 40 and 56) at D = 4, kappa = 0.07125, the lower end of the jump
# method's bracket, started from the jump method's background at kappa_c as in queue 5.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter
cd "$(dirname "$0")"
G=$(python -c "import json; r=[json.loads(l) for l in open('crit.jsonl')][0]; print('%.12f,%.12f,%.12f'%(r['omega'],r['xh'],r['f0']))")
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') css_scan 0.07125 4 --guess=$G"
nice -n 10 python $M/css_scan.py 0.07125 4 --guess=$G --D0=4 --N 40,56 --out=scan_D4_lo.jsonl; echo "== exit $?"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
