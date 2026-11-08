#!/bin/bash
# Issue #145: solver/rt/rt_roots.py on each pair of roots of one grid at one D (logs in controls/roots_*.log).
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
one() {   # one TAG A B
    nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_roots.py "$2" "$3" > "$HERE/controls/roots_$1.log" 2>&1
    echo "$1 exit $?"
    sed -n 2,3p "$HERE/controls/roots_$1.log"
}
one 141_D40 "$HERE/fol/fol_32x141_D40.0201_32x141.npz" "$HERE/controls/from101_32x141_D40.0201_32x141.npz"
one 121_D40 "$HERE/fol/fol_32x121_D40.0201_32x121.npz" "$HERE/controls/from141_32x121_D40.0201_32x121.npz"
one 101_D40 "$HERE/cont/cont_32x101_D40.0201_32x101.npz" "$HERE/controls/from121_32x101_D40.0201_32x101.npz"
one 101_D45 "$HERE/cont/cont_32x101_D44.9634_32x101.npz" "$HERE/fol/from121_32x101_D44.9634_32x101.npz"
one 121_D45 "$HERE/fol/fol_32x121_D44.9634_32x121.npz" "$HERE/fol/from141_32x121_D44.9634_32x121.npz"
one 101_D50 "$HERE/cont/cont_32x101_D50.0075_32x101.npz" "$HERE/fol/from121_32x101_D50.0075_32x101.npz"
one 121_D50a "$HERE/fol/fol_32x121_D50.0075_32x121.npz" "$HERE/fol/from101b_32x121_D50.0075_32x121.npz"
one 121_D50b "$HERE/fol/fol_32x121_D50.0075_32x121.npz" "$HERE/fol/from141_32x121_D50.0075_32x121.npz"
one 101_D55 "$HERE/cont/cont_32x101_D54.9961_32x101.npz" "$HERE/fol/from121_32x101_D54.9961_32x101.npz"
one 121_D55 "$HERE/fol/fol_32x121_D54.9961_32x121.npz" "$HERE/fol/from101b_32x121_D54.9961_32x121.npz"
one 101_D60 "$HERE/cont/cont_32x101_D60.0020_32x101.npz" "$HERE/fol/from121_32x101_D60.0020_32x101.npz"
