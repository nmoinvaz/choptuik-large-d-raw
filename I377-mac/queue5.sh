#!/bin/bash
# I377 queue 5: D = 4 checks of kappa_c(4) first (collocation, an independent discretization, at kappa = 0.0754, kappa_c,
# 0.076; and gamma at kappa = 10 against HE97's Table 1 by both methods), then queue 4's remaining paths (D = 6, 10, 20,
# 40), the D = infinity kappa path and I376's conjugation check.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter
P=$M/css_kappa_crit.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
# collocation (css_scan.py, N = 40 and 56) at D = 4 near kappa_c, started from the jump method's background at kappa_c
G=$(python -c "import json; r=[json.loads(l) for l in open('crit.jsonl')][0]; print('%.12f,%.12f,%.12f'%(r['omega'],r['xh'],r['f0']))")
for k in 0.0754 0.0757329315 0.076; do
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') css_scan $k 4 --guess=$G"
  nice -n 10 python $M/css_scan.py $k 4 --guess=$G --D0=4 --N 40,56 --out=scan_D4.jsonl; echo "== exit $?"
done
# gamma at kappa = 10 (HE97 Table 1: 0.1469): background continued from kappa = 0, then collocation and the jump method
run bgpath 4 10 --h=0.25 --out=bgpath_D4_k10.jsonl
G10=$(python -c "import json; r=[json.loads(l) for l in open('bgpath_D4_k10.jsonl')][-1]; print('%.12f,%.12f,%.12f'%(r['omega'],r['xh'],r['f0'])) if abs(r['kappa']-10)<1e-9 else print('none')")
echo "== kappa 10 background: $G10"
if [ "$G10" != none ]; then
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') css_scan 10 4"
  nice -n 10 python $M/css_scan.py 10 4 --guess=$G10 --D0=4 --N 40,56 --out=scan_D4.jsonl; echo "== exit $?"
  OM=$(echo $G10 | cut -d, -f1); F0=$(echo $G10 | cut -d, -f3)
  for R in 0.85 0.6; do
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') css_pert 4 10 $OM $F0 6.8 0 $R"
    nice -n 10 python $M/css_pert.py 4 10 $OM $F0 6.8 0 $R 2>&1 | tail -1; echo "== exit $?"
  done
fi
run path 6 0.35168333+4.09789715j 2.2695762470 --k1=1 --h=0.01 --out=path_D6.jsonl
run crit path_D6.jsonl 6 --out=crit.jsonl
run path 10 0.42514655+4.99934510j 2.1646154815 --k1=1 --h=0.01 --out=path_D10.jsonl
run crit path_D10.jsonl 10 --out=crit.jsonl
run path 20 0.47996170+6.06910951j 2.0973011405 --k1=1 --h=0.01 --out=path_D20.jsonl
run crit path_D20.jsonl 20 --out=crit.jsonl
run path 40 0.5077925+6.8452800j 2.0565169094 --k1=1 --h=0.01 --out=path_D40.jsonl
run crit path_D40.jsonl 40 --out=crit.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') inner kpath"
nice -n 10 python $M/css_inner_pert.py kpath 0 1 0.05 0.5365223424+7.9320241697j --set=A,B --out=kpath_inf.jsonl
echo "== exit $?"
/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i376/queue3.sh > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i376/queue3.log 2>&1
echo "== queue3 exit $?"
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
