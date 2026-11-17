#!/usr/bin/env bash
# #927 pilot references on the Mac: lowD_highM.py itself from lowD_highM.py's converged pair at D 3.15 (M 128, 160;
# nodes 0.000625..0.9), steps of 0.001 to D 3.149 and 3.148. --diff_max 1 keeps it at M 128/160. A rerun with
# --resume continues it (the progress file ref/leg.jsonl.progress.json).
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a611e0854f7930044/hp || exit 9
echo "ref start $(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" >> $R/ref/exits.txt
nice -n 10 $PY -u lowD_highM.py --start_w $R/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz \
    --start_n $R/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz --Ms 128,160 --dD 0.001 --D_end 3.1476 --diff_max 1 \
    --hours "${HOURS:-0.5}" --point_hours 3 --tag lowD927 --threads 4 --out $R/ref/leg.jsonl --points $R/ref/points.jsonl \
    --states $R/ref/states "$@" >> $R/ref/leg.log 2>&1
echo "ref exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/ref/exits.txt
