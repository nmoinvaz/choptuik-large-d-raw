#!/bin/bash
{
# #1025 lane ISO: the isolation test (svdiso_criteria.log, written first). Lane S's bash (29948) is paused (SIGSTOP) so that its second
# k_c 47 item waits; this lane starts when lane S's current refine (python 69896) ends and resumes lane S at its end.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
trap 'kill -CONT 29948 2>/dev/null; echo "== $(date -u "+%Y-%m-%d %H:%M:%S") lane S resumed"' EXIT
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 5400 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  '; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
while kill -0 69896 2>/dev/null; do sleep 20; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane S's refine 69896 ended"
L13=2.6841484641099442
run $R/svdiso.py data/sol_l1kc31L1025_D13.0000.npy 13 31 $L13; c1=$?
run $R/svdiso.py data/sol_l1kc31L1025_D13.0000.npy 13 31 $L13 --mutate=shift; c2=$?
if [ $c1 -eq 0 ] && [ $c2 -eq 3 ]; then
  echo "== controls read as they must (pass; mutation fails)"
  run $R/svdiso.py data/sol_l1kc55Fs1025_D17.0000.npy 17 55 2.025718689014619
else
  echo "== CONTROL MISREAD (exit $c1, mutation exit $c2): the D 17 run does not start"
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane ISO done"
exit
}
