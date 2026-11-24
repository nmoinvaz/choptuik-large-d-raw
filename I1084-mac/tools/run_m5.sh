#!/bin/bash
# #1084: the M = 5 centre (A 2.726475885672135, wf 1.0156030949093042) from the old log's solved v rounded to 10
# digits, old code under probe.py and then the new code under drive.py, pointv's iters 8
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1084
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3aa6f99477123b54/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_OPERATION_COUNT=1
V=0.1461732092,0.01423943566,0.008040315601,0.001389551001
cd "$S" || exit 1
date -u '+start old_m5 %F %T'
nice -n 10 timeout 3600 "$PY" tools/probe.py "$S/old" pointv 2.726475885672135 1.0156030949093042 --M=5 --v=$V --iters=8 --log=runs/probe_m5.jsonl > runs/probe_m5.out 2> runs/probe_m5.err
echo "old_m5 exit $?"
date -u '+start new_m5 %F %T'
nice -n 10 timeout 3600 "$PY" tools/drive.py "$W" pointv 2.726475885672135 1.0156030949093042 --M=5 --v=$V --iters=8 > runs/new_m5.out 2> runs/new_m5.err
echo "new_m5 exit $?"
date -u '+end %F %T'
exit 0
}
