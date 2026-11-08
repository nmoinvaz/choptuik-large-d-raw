#!/bin/bash
# Issue #163: the symbolic and planted checks of solver/rt/rt_horizon.py and their controls, into checks/.
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aed8a75ee3273b565
RAW=/Users/nathan/Source/choptuik-large-d-raw
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY="nice -n 10 /Users/nathan/venv-qd/bin/python"
cd "$CODE" || exit 2
mkdir -p "$HERE/checks"
run() {   # run LOG command...
    local log=$1; shift
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC $* (code $(git rev-parse --short HEAD))" > "$HERE/checks/$log"
    "$@" >> "$HERE/checks/$log" 2>&1
    echo "== exit $?" >> "$HERE/checks/$log"
    tail -1 "$HERE/checks/$log"
}
S50=$RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz
run symbolic.log $PY solver/rt/rt_horizon.py symbolic "$S50"
run symbolic_mutate_a4.log $PY solver/rt/rt_horizon.py symbolic "$S50" --mutate=a4
run exponents.log $PY solver/rt/rt_horizon.py exponents $RAW/I91-mac/accept/accept_D4.0000_48x81.npz \
    $RAW/I91-mac/accept/accept_D6.0000_32x61.npz $RAW/I91-mac/accept/accept_D8.0000_32x61.npz \
    $RAW/I91-mac/accept/accept_D10.0000_48x81.npz $RAW/I105-mac/cont/cont_32x101_D15.0000_32x101.npz \
    $RAW/I105-mac/cont/cont_32x101_D20.0000_32x101.npz $RAW/I105-mac/cont/cont_32x101_D25.0000_32x101.npz \
    $RAW/I105-mac/cont/cont_32x101_D30.0000_32x101.npz $RAW/I145-mac/cont/cont_32x101_D35.0000_32x101.npz \
    $RAW/I145-mac/cont/cont_32x101_D40.0000_32x101.npz $RAW/I145-mac/cont/cont_32x101_D45.0000_32x101.npz \
    $RAW/I145-mac/cont/cont_32x101_D50.0075_32x101.npz $RAW/I145-mac/cont/cont_32x101_D54.9961_32x101.npz \
    $RAW/I145-mac/cont/cont_32x101_D60.0020_32x101.npz
run planted.log $PY solver/rt/rt_horizon.py planted --raw $RAW --out "$HERE/checks/planted.jsonl"
run planted_mutate_taylor.log $PY solver/rt/rt_horizon.py planted --raw $RAW --mutate=taylor \
    --out "$HERE/checks/planted.jsonl"
