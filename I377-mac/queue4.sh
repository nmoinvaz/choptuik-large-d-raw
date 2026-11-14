#!/bin/bash
# I377 queue 4 (queue 2's paths rerun after the fix of the kappa-history bug; queue 2's log is in failed_v1/):
# the kappa-model CSS's oscillatory mode followed in kappa at D = 4, 6, 10, 20, 40 and kappa_c(D); then the D = infinity
# kappa path; then I376's conjugation check (queue3.sh in the I376 folder).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_kappa_crit.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
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
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') inner kpath"
nice -n 10 python /Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py kpath 0 1 0.05 0.5365223424+7.9320241697j --set=A,B --out=kpath_inf.jsonl
echo "== exit $?"
/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i376/queue3.sh > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/i376/queue3.log 2>&1
echo "== queue3 exit $?"
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
