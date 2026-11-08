#!/bin/bash
# The second process of issue #145 from 10:58 UTC (replaces run_worker3.sh, whose rule 3 started 32x121 from the 32x101
# state a whole unit of D below the check D: at 44.96 max|F| was 3.2e-3 and Newton diverged, stopped by hand). One queue of re-solves (rt_run.py --start STATE --grids 32xN), in order:
#   1. a 32x101 continuation state at a check D           -> 32x121 (fol/fol_32x121)
#   2. a 32x121 state at a check D                        -> 32x101 (fol/from121_32x101): is the 101 root unique?
#   3. the second 32x101 root at a check D (fol/from121_32x101) -> 32x121 (fol/from101b_32x121): a second start for
#      the 32x121 root, so is it unique?
#   3b. a 32x141 state at a check D                       -> 32x121 (fol/from141_32x121): another second start
#   4. a 32x121 state at a check D                        -> 32x141 (fol/fol_32x141)
#   5. the newest 32x101 continuation state               -> 32x121
# It stops when the file STOP_worker exists in this folder.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
CHECKS="D34.9933 D40.0201 D44.9634 D50.0075 D54.9961 D60.0020 D64.9948 D70.0000 D75.0000 D80.0000 D85.0000 D90.0000 D95.0000 D100.0000"
CHECKV="34.993266 40.020065 44.963411 50.007491 54.996085 60.001952 64.994829"
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
OPTS="--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
cd "$CODE" || exit 2

dof() { basename "$1" | sed -E 's/.*_(D[0-9.]+)_[0-9]+x[0-9]+\.npz/\1/'; }

pick() {   # pick GLOB TAG ONLYCHECK -> prints the chosen state or nothing
    local f d
    for f in $(ls -t $1 2>/dev/null); do
        d=$(dof "$f")
        [ -e "$HERE/fol/done_${2}_$d" ] && continue
        [ $(( $(date +%s) - $(stat -f %m "$f") )) -lt 10 ] && continue        # still being written
        if [ "$3" = 1 ]; then
            case " $CHECKS " in *" $d "*) echo "$f"; return;; esac
        else
            echo "$f"; return
        fi
    done
}

pick_int() {   # rule 3: a check D whose 32x101 state and integer-D state exist -> "INTSTATE CHECKD DTAG"
    local v d i f
    for v in $CHECKV; do
        d="D$(printf '%.4f' "$v")"
        [ -e "$HERE/fol/done_fromint_32x121_$d" ] && continue
        [ -e "$HERE/cont/cont_32x101_${d}_32x101.npz" ] || continue
        i=$(printf '%.4f' "${v%.*}")
        f="$HERE/cont/cont_32x101_D${i}_32x101.npz"
        [ -e "$f" ] && { echo "$f $v $d"; return; }
    done
}

run() {   # run STATE N TAG DTAG [D_START]
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC worker: $1 on 32x$2 ($3)${5:+ at D $5}"
    nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$1" ${5:+--D_start $5} --grids "32x$2" \
        $OPTS --out "$HERE/fol" --tag "$3"
    echo "== exit $? for $3 $4"
    touch "$HERE/fol/done_${3}_$4"
}

while [ ! -e "$HERE/STOP_worker" ]; do
    st=$(pick "$HERE/cont/cont_32x101_D*.npz" fol_32x121 1)
    if [ -n "$st" ]; then run "$st" 121 fol_32x121 "$(dof "$st")"; continue; fi
    st=$(pick "$HERE/fol/fol_32x121_D*.npz" from121_32x101 1)
    if [ -n "$st" ]; then run "$st" 101 from121_32x101 "$(dof "$st")"; continue; fi
    st=$(pick "$HERE/fol/from121_32x101_D*.npz" from101b_32x121 1)
    if [ -n "$st" ]; then run "$st" 121 from101b_32x121 "$(dof "$st")"; continue; fi
    st=$(pick "$HERE/fol/fol_32x141_D*.npz" from141_32x121 1)
    if [ -n "$st" ]; then run "$st" 121 from141_32x121 "$(dof "$st")"; continue; fi
    st=$(pick "$HERE/fol/fol_32x121_D*.npz" fol_32x141 1)
    if [ -n "$st" ]; then run "$st" 141 fol_32x141 "$(dof "$st")"; continue; fi
    st=$(pick "$HERE/cont/cont_32x101_D*.npz" fol_32x121 0)
    if [ -n "$st" ]; then run "$st" 121 fol_32x121 "$(dof "$st")"; continue; fi
    sleep 30
done
