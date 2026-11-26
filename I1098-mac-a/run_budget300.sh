#!/bin/bash
# #1098 part 1: D 300's full solve re-solved per discretization variant (base, steps2, ks+200, kc+20, kt+8) by
# release_ls --harm 13 --kmax 13 from the variant state, octo-double residual, tol 1e-48, tol_h 1e-44, the qd Jacobian
# with the hand-over to qq; one variant after another on the Mac (2 threads, nice 10)
{
H=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1088a
O=/Users/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-mac-a/budget300
cd $H || exit 1
for v in base steps2 ks+200 kc+20 kt+8; do
  mkdir -p $O/$v
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$v/run.log
  PYTHONPATH=$S/site_g OPENBLAS_NUM_THREADS=2 nice -n 10 /Users/nathan/venv-314/bin/python -u form_s.py release_ls \
    $S/budget/D300_full_$v.npz $O/$v --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 2 \
    --outer 6 --commit 992c86c3 2>&1 | grep --line-buffered -vE "^thread|^note:|slaving LU" > $O/$v/rls.log
  echo "rc ${PIPESTATUS[0]}" >> $O/$v/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$v/run.log
done
exit
}
