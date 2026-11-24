#!/bin/bash
# the old code (feat/inner-mp 6b807830, value_mp.py and inner_mp.py as is) under probe.py on #1076 points p2, p3
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1084
PY=/Users/nathan/venv-314/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_OPERATION_COUNT=1
cd "$S" || exit 1
while pgrep -f "probe.py.*probe_p1" >/dev/null; do sleep 5; done
date -u '+start p2 %F %T'
nice -n 10 timeout 2400 "$PY" tools/probe.py "$S/old" point 3.553347058422 0.413172823632 0.006041017694051223 -0.3799219466832089 --iters=12 --log=runs/probe_p2.jsonl > runs/probe_p2.out 2> runs/probe_p2.err
echo "p2 exit $?"
date -u '+start p3 %F %T'
nice -n 10 timeout 2400 "$PY" tools/probe.py "$S/old" point 3.5529706 0.41289086625 0.006040267478291 -0.380031415605351 --iters=12 --log=runs/probe_p3.jsonl > runs/probe_p3.out 2> runs/probe_p3.err
echo "p3 exit $?"
date -u '+end %F %T'
exit 0
}
