#!/bin/bash
{
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a/site_m FORMS_HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=2
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-1090/solver/inner_large_d
while kill -0 51720 2>/dev/null; do sleep 30; done
date -u '+start %Y-%m-%d %H:%M:%S UTC'
run() { out=$1; shift; nice -n 10 $PY -u hp_mob_check.py /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/cedd07ca-f64a-4d93-bd85-b22c2929be53/scratchpad/raw1090live/I1090-mac/f64_M6_cont3/sol_D646_M6_a8.json /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/cedd07ca-f64a-4d93-bd85-b22c2929be53/scratchpad/raw1090live/I1090-mac/diag/trackc_at.json --guess=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/cedd07ca-f64a-4d93-bd85-b22c2929be53/scratchpad/raw1090live/I1090-mac/hp_mob/guess_mh.json "$@" > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/cedd07ca-f64a-4d93-bd85-b22c2929be53/scratchpad/raw1090live/I1090-mac/hp_mob/$out.log 2>&1; echo "exit $?" >> /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/cedd07ca-f64a-4d93-bd85-b22c2929be53/scratchpad/raw1090live/I1090-mac/hp_mob/$out.log; date -u "+done $out %H:%M:%S UTC"; }
run g_D1000_2000 --Ds=1000,2000
run g_D5000_inv --Ds=5000 --gain=0 --hp_inv=1
run g_D5000_a8 --Ds=5000 --gain=0 --a_fixed=8
run g_D10000 --Ds=10000 --gain=0
run g_D10000_a8 --Ds=10000 --gain=0 --a_fixed=8
date -u '+end %Y-%m-%d %H:%M:%S UTC'
exit
}
