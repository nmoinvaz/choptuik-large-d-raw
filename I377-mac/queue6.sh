#!/bin/bash
# I377 queue 6: kappa_c at D = infinity refined from the inner kappa path (css_inner_pert.py kcrit), settings A and B
source ~/venv-314/bin/activate
cd "$(dirname "$0")"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') kcrit"
nice -n 10 python /Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py kcrit kpath_inf.jsonl --set=A,B --out=kcrit_inf.jsonl
echo "== exit $?"
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
