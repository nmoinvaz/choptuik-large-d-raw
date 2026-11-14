#!/bin/bash
# I770 queue 1 at kappa = 1, omega_inf = 3.1998939, eps = 1/4 (box B at setting A ran in pilot.sh):
#   A  0.05 < Re < 0.9, |Im| < omega - eps          expected none
#   B  0.9  < Re < 5,   |Im| < omega - eps          expected lambda = 1, 2
#   S  0.05 < Re < 5,   omega - eps < Im < omega + eps      expected none (upper half; conjugation covers the lower)
#   C  0.05 < Re < 5,   omega + eps < Im < 3 omega          expected none (lambda_osc is damped at kappa = 1)
#   W  0.05 < Re < 8,   |Im| < 3 omega                      expected lambda = 1, 2
# then the controls: a zero planted at 3 + 1i in B (must count 3), and --mutate=nometric in B (must change B).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
OL=2.9498939; OH=3.4498939; O3=9.5996817
run count 1 0.9 5 -$OL $OL --set=B --out=counts_k1.jsonl
run count 1 0.05 0.9 -$OL $OL --set=A,B --out=counts_k1.jsonl
run count 1 0.05 5 $OL $OH --set=A,B --out=counts_k1.jsonl
run count 1 0.05 5 $OH $O3 --set=A,B --out=counts_k1.jsonl
run count 1 0.9 5 -$OL $OL --set=A --plant=3+1j --out=controls_k1.jsonl
run count 1 0.9 5 -$OL $OL --set=A --mutate=nometric --out=controls_k1.jsonl
run count 1 0.05 8 -$O3 $O3 --set=A,B --out=counts_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
