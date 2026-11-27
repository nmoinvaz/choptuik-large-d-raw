#!/bin/bash
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
I=$W/in; V=$W/A/valley
cd /Users/nathan/Source/choptuik-1101w/solver/matter
export VECLIB_MAXIMUM_THREADS=2
L=2.10,2.18,2.22,2.24,2.25,2.26,2.30,2.40
for spec in "u40 $I/l1kc55u040.jsonl $I/sol_l1kc55u040_D16.0000.npy" "v01 $V/sol_v01_D16.0000.jsonl $V/sol_v01_D16.0000.npy" "v10 $V/sol_v10_D16.0000.jsonl $V/sol_v10_D16.0000.npy"; do
  set -- $spec
  echo "== $1"
  nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py locate $2 $3 16.0 $L 2>&1 | grep -v Warning
done
