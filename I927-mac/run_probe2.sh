#!/usr/bin/env bash
# #927 probe 2 on the Mac: the controls of probe 1 (fixed_plan/d304315). (a) the order-3 sum at D 3.04335 and 3.04325
# and 3.04315 on the base's plan (finite expected at 3.04335, where #343 converged; 3.04315 again for the segments); (b) at D 3.04315 the two states the leg had,
# the base state of the series (order 0, D 3.04375) and I343's converged 3.04335 state (the Lagrange predictor through
# that one state is the state itself, lowD_highM.py's "last state" start), on the 3.04335 state's plan.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a611e0854f7930044/hp || exit 9
nice -n 10 $PY -u lowD_fixed_plan.py $R $R/I927-mac/fixed_plan/onset --coeffs I798-win/probe/coeffs.npz \
    --targets 3.04335,3.04325,3.04315 --orders 3 --plans base --threads 4 > $R/I927-mac/fixed_plan/onset.log 2>&1
echo "onset exit $?" >> $R/I927-mac/fixed_plan/probe2_exits.txt
nice -n 10 $PY -u lowD_fixed_plan.py $R $R/I927-mac/fixed_plan/last_state --coeffs I798-win/probe/coeffs.npz \
    --targets 3.04315 --orders 0 --plans I343-win2/states/lowD343_D3.043350_M384.npz \
    --hist I343-win2/states/lowD343_D3.043350_M384.npz --threads 4 > $R/I927-mac/fixed_plan/last_state.log 2>&1
echo "last_state exit $?" >> $R/I927-mac/fixed_plan/probe2_exits.txt
