#!/bin/bash
# I95-mac: the zeros of the resonance strip S located and tested at the second radius (complex_css.py locate), and
# the collocation spectrum at kappa = 0, D = 4-8 (css_scan.py, independent of the jump method)
PY=/Users/nathan/venv-qd/bin/python
M=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac/css
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY "$@"; echo "exit $?"; }
run $M/complex_css.py locate 4 0.05 5.0 1.6654446898931115 2.1654446898931115 --out=$R/locate_k0.jsonl
run $M/css_scan.py 0 4,5,6,8 --N 40,56 --out $R/scan_k0.jsonl
run $M/complex_css.py locate 5 0.05 5.0 1.7866663578112 2.2866663578112 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 6 0.05 5.0 1.9262864130458 2.4262864130458 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 8 0.05 5.0 2.16204238630221 2.66204238630221 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 10 0.05 5.0 2.34334850089595 2.84334850089595 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 20 0.05 5.0 2.84462326541277 3.34462326541277 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 40 0.05 5.0 3.21151262290065 3.71151262290065 --out=$R/locate_k0.jsonl
run $M/complex_css.py locate 80 0.05 5.0 3.44509638099619 3.94509638099619 --out=$R/locate_k0.jsonl
