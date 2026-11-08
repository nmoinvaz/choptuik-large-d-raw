#!/bin/bash
# Issue #164: one worker of the re-solves. Solves the RT prototype on each grid at D 60.001952 and then 54.996085,
# from one start resampled (a: the 32x101 continuation state of I145, b: the 32x121 root of I145's follower).
#   run_main.sh a|b "32x85 32x91 32x95" [D60.0020 D54.9961]
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3f8a38336503b3e7
I145=/Users/nathan/Source/choptuik-large-d-raw/I145-mac
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
cd "$CODE" || exit 2
S=$1
GRIDS=$2
shift 2
DTAGS=${*:-D60.0020 D54.9961}
OPTS="--solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
mkdir -p "$HERE/roots"
for DTAG in $DTAGS; do
    case $DTAG in
        D60.0020) NTOL=1e-36 ;;
        D54.9961) NTOL=1e-38 ;;
        *) echo "unknown D $DTAG"; exit 2 ;;
    esac
    if [ "$S" = a ]; then
        ST="$I145/cont/cont_32x101_${DTAG}_32x101.npz"; TAG=a101
    else
        ST="$I145/fol/fol_32x121_${DTAG}_32x121.npz"; TAG=b121
    fi
    for G in $GRIDS; do
        echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC ${TAG}_$G $DTAG"
        nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$ST" --grids "$G" $OPTS \
            --newton_tol $NTOL --out "$HERE/roots" --tag "${TAG}_$G"
        echo "== exit $? ${TAG}_$G $DTAG"
    done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC done"
