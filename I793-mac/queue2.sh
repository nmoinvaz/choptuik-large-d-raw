#!/bin/bash
# I793 queue 2: COMPLEX_CRITICAL 2's sub-box windings of the strip S (complex_css.py locate, sub-boxes of width 0.5,
# each zero refined at R = 0.6 x_h), the same commands as I95-mac/css/queue5.sh, with the new default.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-793/solver/matter
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$M/complex_css.py" "$@"; echo "== exit $?"; }
O=locate_k0.jsonl
run locate 4 0.05 5.0 1.6654446898931115 2.1654446898931115 --out=$O
run locate 5 0.05 5.0 1.7866663578112 2.2866663578112 --out=$O
run locate 6 0.05 5.0 1.9262864130458 2.4262864130458 --out=$O
run locate 8 0.05 5.0 2.16204238630221 2.66204238630221 --out=$O
run locate 10 0.05 5.0 2.34334850089595 2.84334850089595 --out=$O
run locate 20 0.05 5.0 2.84462326541277 3.34462326541277 --out=$O
run locate 40 0.05 5.0 3.21151262290065 3.71151262290065 --out=$O
run locate 80 0.05 5.0 3.44509638099619 3.94509638099619 --out=$O
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
