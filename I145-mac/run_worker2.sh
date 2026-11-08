#!/bin/bash
# The second process of issue #145 from 10:20 UTC (replaces run_worker.sh): one queue of re-solves, each a state
# resampled to another grid and re-solved there at its D (rt_run.py --start STATE --grids 32xN). In order:
#   1. a 32x101 continuation state at a check D  -> 32x121 (fol/fol_32x121)
#   2. a 32x121 state at a check D               -> 32x141 (fol/fol_32x141)
#   3. a 32x121 state at a check D               -> 32x101 (fol/from121_32x101): is the 101 root unique?
#   4. a 32x141 state at a check D               -> 32x121 (fol/from141_32x121): is the 121 root unique?
#   5. the newest 32x101 continuation state      -> 32x121
# It stops when the file STOP_worker exists in this folder.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
CHECKS="D34.9933 D40.0201 D44.9634 D50.0075 D54.9961 D60.0020 D64.9948 D70.0000 D75.0000 D80.0000 D85.0000 D90.0000 D95.0000 D100.0000"
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
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

while [ ! -e "$HERE/STOP_worker" ]; do
    st=""
    for rule in "cont/cont_32x101_D*.npz fol_32x121 121 1" "fol/fol_32x121_D*.npz fol_32x141 141 1" \
                "fol/fol_32x121_D*.npz from121_32x101 101 1" "fol/fol_32x141_D*.npz from141_32x121 121 1" \
                "cont/cont_32x101_D*.npz fol_32x121 121 0"; do
        set -- $rule
        st=$(pick "$HERE/$1" "$2" "$4"); TAG=$2; N=$3
        [ -n "$st" ] && break
    done
    if [ -z "$st" ]; then sleep 30; continue; fi
    d=$(dof "$st")
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC worker: $st on 32x$N ($TAG)"
    nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$st" --grids "32x$N" --solver mp \
        --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 \
        --out "$HERE/fol" --tag "$TAG"
    echo "== exit $? for $TAG $d"
    touch "$HERE/fol/done_${TAG}_$d"
done
