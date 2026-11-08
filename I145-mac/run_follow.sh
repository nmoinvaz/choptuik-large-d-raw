#!/bin/bash
# The follower of issue #145: re-solves each state that a continuation saves (cont/<SRC_TAG>_D*.npz) on 32 x N,
# from that state resampled (rt_run.py --start STATE --grids 32xN, one Newton solve at the state's D), the check D
# first and otherwise the newest state not yet done. It stops when the file STOP_<TAG> exists in this folder.
#   run_follow.sh N SRC_TAG TAG
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5b009d60d38d2338
N="$1"; SRC="$2"; TAG="$3"
CHECKS="D34.9933 D40.0201 D44.9634 D50.0075 D54.9961 D60.0020 D64.9948 D70.0000 D75.0000 D80.0000 D85.0000 D90.0000 D95.0000 D100.0000"
mkdir -p "$HERE/fol"
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
while [ ! -e "$HERE/STOP_$TAG" ]; do
    pick=""
    for f in $(ls -t "$HERE"/cont/"$SRC"_D*.npz 2>/dev/null); do
        d=$(basename "$f" | sed -E 's/.*_(D[0-9.]+)_32x[0-9]+\.npz/\1/')
        [ -e "$HERE/fol/done_${TAG}_$d" ] && continue
        [ $(( $(date +%s) - $(stat -f %m "$f") )) -lt 10 ] && continue        # still being written
        [ -z "$pick" ] && pick="$f"
        case " $CHECKS " in *" $d "*) pick="$f"; break;; esac
    done
    if [ -z "$pick" ]; then sleep 30; continue; fi
    d=$(basename "$pick" | sed -E 's/.*_(D[0-9.]+)_32x[0-9]+\.npz/\1/')
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC follow $pick on 32x$N"
    nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$pick" --grids "32x$N" --solver mp \
        --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --out "$HERE/fol" --tag "$TAG"
    echo "== exit $? for $d"
    touch "$HERE/fol/done_${TAG}_$d"
done
