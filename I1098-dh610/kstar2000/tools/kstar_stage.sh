#!/bin/bash
# #1098 ladder, the k* stage (the last stage of ladder_point2.sh and ladder_tail.sh): err_resid, the first-order bound
# on Delta at kfree k* (KSTAR, 15 by default), is gain(k*) x the k* system's |F| at h<k*>'s release. The tail's tol
# 1e-48 does not make it small: D 622 released h15 at |F| 3.41e-51 with gain 1.05e28, a bound of 3.6e-23. So:
#   1. kstar_gain.py: the gain at kfreeze k* at the tail's final state (its highest release_ls_h<k>_D<D>.npz);
#   2. when gain x F(k*) > 1e-27: the k* system re-converged from the h<k*> state by release_ls --harm k* --kmax k*
#      (its target system is kfreeze k*, kstar_gain.py's), qq, od, tol 1e-62, into OUT;
#   3. kstar_summary.py: OUT/kstar.json with the bound before and after (gain x F_after + |the move of Delta|), which
#      ladder_record.py --kstar_json reads
#
#     [KSTAR=15] kstar_stage.sh TAILDIR OUT THREADS
{
TD=$1; O=$2; T=$3; K=${KSTAR:-15}
HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
SITE=${SITE:-$HOME/Source/fastmul6-site}
PY=${PY:-$HOME/venv-314/bin/python}
EXTRA=${EXTRA:-}
IC=${INNER_CHORD:-0}
COMMIT=${COMMIT:-$(git -C $HP rev-parse --short=8 HEAD 2>/dev/null || echo unknown)}
TOOLS=$(cd "$(dirname "$0")" && pwd)
[ -s "$TD/release_ls.jsonl" ] && [ -n "$T" ] || { echo "usage: kstar_stage.sh TAILDIR OUT THREADS"; exit 1; }
mkdir -p $O
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
FIN=$(ls $TD/release_ls_h*_D*.npz | grep -v _step | awk -F_h '{split($NF, a, "_"); print a[1], $0}' | sort -n | tail -1 | cut -d' ' -f2)
RK=$(ls $TD/release_ls_h${K}_D*.npz | grep -v _step | head -1)
[ -s "$FIN" ] && [ -s "$RK" ] || exit 2
echo "k* $K: final state $(basename $FIN), h$K state $(basename $RK) ($(date -u +%H:%M:%S))" > $O/run.log
PYTHONPATH=$SITE:$HP nice -n 10 $PY -u $TOOLS/kstar_gain.py $FIN --kfreeze $K --threads $T > $O/gain.log 2>&1 || exit 3
G=$(grep -oE "^gain_qd [0-9.e+-]+" $O/gain.log | awk '{print $2}')
[ -n "$G" ] || exit 3
PYTHONPATH=$SITE:$HP $PY $TOOLS/kstar_summary.py $TD/release_ls.jsonl $K $G $O/kstar.json >> $O/run.log 2>&1 || exit 4
if $PY -c "import json, sys; sys.exit(0 if json.load(open('$O/kstar.json'))['bound_before'] > 1e-27 else 1)"; then
  cd $HP || exit 1
  nice -n 10 timeout 3h $PY -u form_s.py release_ls $RK $O --harm $K --kmax $K --jac qq --res od --tol 1e-62 \
    --tol_h 1e-50 --ddelta 1e-40 --threads $T --outer 4 --inner_chord $IC --commit $COMMIT $EXTRA > $O/rls.log 2>&1
  echo "reconv rc $? $(date -u +%H:%M:%S)" >> $O/run.log
  PYTHONPATH=$SITE:$HP $PY $TOOLS/kstar_summary.py $TD/release_ls.jsonl $K $G $O/kstar.json $O/release_ls.jsonl $RK \
    >> $O/run.log 2>&1 || exit 5
else
  echo "bound at k* within 1e-27: no re-converge ($(date -u +%H:%M:%S))" >> $O/run.log
fi
exit
}
