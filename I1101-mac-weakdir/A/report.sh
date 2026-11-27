#!/bin/bash
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101
I=$W/in
cd /Users/nathan/Source/choptuik-1101w/solver/matter
export VECLIB_MAXIMUM_THREADS=2
U="$I/l1kc55u040.jsonl:$I/sol_l1kc55u040_D16.0000.npy"
ARGS="src=$I/l1kc55Fb1025.jsonl:$I/sol_l1kc55Fb1025_D16.0000.npy U40=$U U40b=$I/l1kc55u040b.jsonl:$I/sol_l1kc55u040b_D16.0000.npy U40c=$I/l1kc55u040c.jsonl:$I/sol_l1kc55u040c_D16.0000.npy P52=$U+1e-3@52 M52=$U+-1e-3@52 P53=$U+1e-3@53 M53=$U+-1e-3@53 P52c=$U+3e-3@52 M52c=$U+-3e-3@52"
tag=${1:-}
mut=${2:-}
nice -n 10 /Users/nathan/venv-1025dd/bin/python -u i1101_weakdir.py report $W/jac/J_src.npz $W/jac/svd_src.npz 16.0 $ARGS --out=$W/A/report_src$tag.json $mut > $W/A/report_src$tag.log 2>&1
echo "report exit $?" >> $W/A/report_src$tag.log
