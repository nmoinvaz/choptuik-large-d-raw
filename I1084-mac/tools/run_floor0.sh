#!/bin/bash
# #1084 (d): the new code with --floor=0 on p2, after run_new.sh; its row and calls against the old code's
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1084
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3aa6f99477123b54/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_OPERATION_COUNT=1
while pgrep -f "tools/run_new.sh" >/dev/null; do sleep 5; done
cd "$S" || exit 1
date -u '+start floor0_p2 %F %T'
nice -n 10 timeout 3600 "$PY" tools/drive.py "$W" point 3.553347058422 0.413172823632 0.006041017694051223 -0.3799219466832089 --iters=12 --floor=0 > runs/floor0_p2.out 2> runs/floor0_p2.err
echo "floor0_p2 exit $?"
date -u '+end %F %T'
exit 0
}
