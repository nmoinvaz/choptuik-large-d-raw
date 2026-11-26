#!/bin/bash
# #1098 part 1, the M budget at D 300: mm5's full kfree-31 state (I1098-mm5/kfree300, M 32) resampled to M 48
# (resample_m.py) and re-converged at M 48 by release_ls --harm 31 --kmax 31 (the inner solve frees every harmonic
# below 31, so the whole kfree-31 system is re-solved at M 48), the octo-double residual, tol 1e-48, the qd Jacobian
# with the hand-over to qq; the Hamiltonian check at M 48 in the record; the dev-o1 kernel of b9a2954b (site_h); Mac,
# 2 threads
{
H=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a
O=/Users/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-mac-a/m48_300
cd $H || exit 1
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
PYTHONPATH=$S/site_h OPENBLAS_NUM_THREADS=2 nice -n 10 /Users/nathan/venv-314/bin/python -u form_s.py release_ls \
  $S/budget/D300_kfree31_M48.npz $O --harm 31 --kmax 31 --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 2 \
  --outer 6 --commit b9a2954b 2>&1 | grep --line-buffered -vE "^thread|^note:|slaving LU" > $O/rls.log
echo "rc ${PIPESTATUS[0]}" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
