#!/usr/bin/env bash
# #927 pilot references on the Mac: lowD_highM.py itself from a converged pair at consecutive M and the same nodes.
# Default (amendment of 2026-11-17 01:00 UTC, the Mac's load at 100-137): lowDv_D3.7000_M48/M64 (13 nodes
# 0.005..0.8, kc 100, ks 250), steps of 0.005 to D 3.695 and 3.69. PAIR=128 gives the first design: the D 3.15 pair
# (M 128, 160; nodes 0.000625..0.9), steps of 0.001 to 3.149 and 3.148. --diff_max 1 keeps the pair's M. A rerun with
# --resume continues it.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a611e0854f7930044/hp || exit 9
if [ "${PAIR:-48}" = 128 ]; then
    W=$R/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz; N=$R/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz
    ARGS="--Ms 128,160 --dD 0.001 --D_end 3.1476"; OUT=$R/ref
else
    W=$R/inputs/lowDv_D3.7000_M48.npz; N=$R/inputs/lowDv_D3.7000_M64.npz
    ARGS="--Ms 48,64 --dD 0.005 --D_end 3.6876"; OUT=$R/ref48
fi
mkdir -p $OUT
echo "ref start $(date -u '+%Y-%m-%d %H:%M:%S UTC') PAIR ${PAIR:-48} $*" >> $OUT/exits.txt
nice -n 10 $PY -u lowD_highM.py --start_w $W --start_n $N $ARGS --diff_max 1 \
    --hours "${HOURS:-0.5}" --point_hours 3 --tag lowD927 --threads 4 --out $OUT/leg.jsonl --points $OUT/points.jsonl \
    --states $OUT/states "$@" >> $OUT/leg.log 2>&1
echo "ref exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits.txt
