#!/bin/bash
# I376 queue 1: controls, precision checks and box counts of the D = infinity inner CSS perturbations, kappa = 0.
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
# roots: the lambda = 2 control and lambda_osc, three (r0, r1) settings
run root 0 2.1 --out=roots_k0.jsonl
run root 0 0.536+7.93j --out=roots_k0.jsonl
run root 0 1.1 --set=A,B --out=roots_k0.jsonl
# precision: integrator tolerance and series digits
run root 0 0.5365+7.932j --set=A --rtol=1e-13 --out=roots_k0.jsonl
run root 0 0.5365+7.932j --set=A --dps=60 --out=roots_k0.jsonl
# mutations: det M at the exact lambda = 1, 2 and the secant from 2.1
for m in nometric hamsign; do
  for l in 1 2 1.5; do run det 0 $l --mutate=$m --out=mut_k0.jsonl; done
  run root 0 2.1 --set=A --mutate=$m --out=mut_k0.jsonl
done
for l in 1 2 1.5; do run det 0 $l --out=mut_k0.jsonl; done
# box counts (omega = 3.97897, eps = 0.25), settings A and B
OM=3.9789695073723137
run count 0 0.05 0.9 -3.7289695 3.7289695 --set=A,B --out=counts_k0.jsonl
run count 0 0.9 5 -3.7289695 3.7289695 --set=A,B --out=counts_k0.jsonl
run count 0 0.05 5 4.2289695 9.432 --set=A,B --out=counts_k0.jsonl
run count 0 0.05 5 3.7289695 4.2289695 --set=A,B --out=counts_k0.jsonl
# controls of the counts: a planted zero in C, the nometric mutation in B
run count 0 0.05 5 4.2289695 9.432 --set=A --plant=1.0+6.0j --out=counts_k0.jsonl
run count 0 0.9 5 -3.7289695 3.7289695 --set=A --mutate=nometric --out=counts_k0.jsonl
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
