#!/bin/bash
# The six runs of ../tools/h23test.sh (blob f44db4588c08a96014ac1635817bccfceb25fee2), two at a time instead of all at once.
# The `run` function is the script's, unchanged; only the six calls at its end are replaced by a 2-wide queue.
#
#     queue_h23.sh MOB21 U21 OUT [WIDTH]
{
export MOB=$1 U=$2 O=$3
W=${4:-2}
export HP=${HP:-$HOME/Source/choptuik-fastmul6/hp}
export SITE=${SITE:-$HOME/Source/fastmul6-site}
export PY=${PY:-$HOME/venv-314/bin/python}
export EXTRA=${EXTRA:-}
export TOOLS=$(cd "$(dirname "$0")/../tools" && pwd)
[ -s "$MOB" ] && [ -s "$U" ] && [ -d "$O" ] || { echo "usage: queue_h23.sh MOB21 U21 OUT [WIDTH]"; exit 1; }
cd $HP || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
run() {  # name state variant
  mkdir -p $O/$1
  {
    date -u "+start %Y-%m-%d %H:%M:%S UTC"
    PYTHONPATH=$SITE:$HP $PY $TOOLS/variant_state.py $HP $2 $O/$1/start.npz $3
  } > $O/$1/run.log 2>&1
  nice -n 10 timeout 2h $PY -u form_s.py release_ls $O/$1/start.npz $O/$1 --harm 23 --kmax 31 --jac_by 23:qq --res od \
    --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 3 --outer 8 --commit 478e9d86 $EXTRA > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
export -f run
printf '%s\n' "mob_ks800 $MOB ks=800" "mob_ks1000 $MOB ks=1000" "u_ks706 $U ks=706" "mob_a4 $MOB mob4,ks=800" \
  "mob_a6 $MOB mob6,ks=800" "u_ks906 $U ks=906" | xargs -L1 -P $W bash -c 'run "$@"' _
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
exit
}
