#!/bin/bash
# I793 queue 1: COMPLEX_CRITICAL 2's box counts recounted with the new default (one starting sample per 0.25 of edge),
# the same commands as I95-mac/css/queue2.sh: the D = 4 controls, then boxes A, B, C, S at both radii for each D.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-793/solver/matter
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$M/complex_css.py" "$@"; echo "== exit $?"; }
O=boxes_k0.jsonl
run boxes 4 0.25866983+3.50224880j --R=0.85 --names=C --plant=1.0+3.0j --out=$O
run boxes 4 0.25866983+3.50224880j --R=0.85 --names=B,C --mutate=nometric --out=$O
run boxes 4 0.25866983+3.50224880j --out=$O
run boxes 5 0.31462468+3.78948723j --out=$O
run boxes 6 0.35163567+4.09794310j --out=$O
run boxes 8 0.39769776+4.60913768j --out=$O
run boxes 10 0.42514173+4.99931817j --out=$O
run boxes 20 0.47996049+6.06909284j --out=$O
run boxes 40 0.50779164+6.84526018j --out=$O
run boxes 80 0.52199898+7.33689470j --out=$O
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
