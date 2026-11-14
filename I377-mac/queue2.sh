#!/bin/bash
# I377 queue 2: the kappa-model CSS's oscillatory mode followed in kappa at D = 4, 6, 10, 20, 40, and kappa_c(D).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_kappa_crit.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
run selftest
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') css_inner_pert check 0 and 0.5"
for k in 0 0.5; do nice -n 10 python /Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py check $k --out=inner_check.jsonl; echo "== exit $?"; done
# control: the background continued in kappa at D = 4 must end on HHS96's axion-dilaton solution at kappa = 1
run bgpath 4 1 --h=0.05 --out=bgpath_D4.jsonl
# seeds: kappa = 0 roots of matter/COMPLEX_CRITICAL.md section 4 (lambda_osc, lambda_phys)
run path 4 0.2586698339+3.5022487970j 2.5832751746 --k1=1 --h=0.01 --out=path_D4.jsonl
run crit path_D4.jsonl 4 --out=crit.jsonl
run path 6 0.35168333+4.09789715j 2.2695762470 --k1=1 --h=0.01 --out=path_D6.jsonl
run crit path_D6.jsonl 6 --out=crit.jsonl
run path 10 0.42514655+4.99934510j 2.1646154815 --k1=1 --h=0.01 --out=path_D10.jsonl
run crit path_D10.jsonl 10 --out=crit.jsonl
run path 20 0.47996170+6.06910951j 2.0973011405 --k1=1 --h=0.01 --out=path_D20.jsonl
run crit path_D20.jsonl 20 --out=crit.jsonl
run path 40 0.5077925+6.8452800j 2.0565169094 --k1=1 --h=0.01 --out=path_D40.jsonl
run crit path_D40.jsonl 40 --out=crit.jsonl
# D = infinity: lambda_osc of the inner CSS solution followed in kappa (css_inner_pert.py, settings A and B)
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') inner kpath"
nice -n 10 python /Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py kpath 0 1 0.05 0.5365223424+7.9320241697j --set=A,B --out=kpath_inf.jsonl
echo "== exit $?"
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
