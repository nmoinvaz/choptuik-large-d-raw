#!/bin/bash
# I793 queue 3: CSS_STABILITY 1.4 (kappa = 0) and 1.6 (kappa = 1) recounted with the new default, the same boxes as
# I376-mac/queue1.sh and I770-mac/queue1-5.sh; W at kappa = 1 also with K = 6 (the control: it gave 0 at both settings).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-793/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
O=inner_counts.jsonl
# kappa = 0, omega_inf = 3.9789695
run count 0 0.05 0.9 -3.7289695 3.7289695 --set=A,B --out=$O
run count 0 0.9 5 -3.7289695 3.7289695 --set=A,B --out=$O
run count 0 0.05 5 4.2289695 9.432 --set=A,B --out=$O
run count 0 0.05 5 3.7289695 4.2289695 --set=A,B --out=$O
run count 0 0.05 5 4.2289695 9.432 --set=A --plant=1.0+6.0j --out=$O
run count 0 0.9 5 -3.7289695 3.7289695 --set=A --mutate=nometric --out=$O
# kappa = 1, omega_inf = 3.1998939
OL=2.9498939; OH=3.4498939; O3=9.5996817
run count 1 0.05 0.9 -$OL $OL --set=A,B --out=$O
run count 1 0.9 5 -$OL $OL --set=A,B --out=$O
run count 1 0.05 5 $OL $OH --set=A,B --out=$O
run count 1 0.05 5 $OH $O3 --set=A,B --out=$O
run count 1 0.9 5 -$OL $OL --set=A --plant=3+1j --out=$O
run count 1 0.9 5 -$OL $OL --set=A --mutate=nometric --out=$O
run count 1 5 8 -$OL $OL --set=A --out=$O
run count 1 5 8 $OL $O3 --set=A --out=$O
run count 1 6.5 8 2.9498939 4.61234085 --set=B --out=$O
run locate 1 2 3 5.5 6.5 --set=A,B --plant=2.3+6.1j --out=$O
run count 1 0.05 8 -$O3 $O3 --set=A,B --out=$O
run count 1 0.05 8 -$O3 $O3 --set=A,B --K=6 --out=$O
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
