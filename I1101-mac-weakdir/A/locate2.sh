#!/bin/bash
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
V=$W/A/valley
cd /Users/nathan/Source/choptuik-1101w/solver/matter
export VECLIB_MAXIMUM_THREADS=2
L=1.8,2.0,2.1,2.2,2.22,2.24,2.25,2.26,2.28,2.3,2.4,2.6
for nm in w001 w01 w10; do
  echo "== $nm"
  nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py locate $V/sol_${nm}_D16.0000.jsonl $V/sol_${nm}_D16.0000.npy 16.0 $L 2>&1 | grep -v Warning
done
