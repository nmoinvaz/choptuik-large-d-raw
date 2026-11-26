#!/bin/bash
# #1098: the budget re-measured on a kernel with lane-precision reciprocals (33eeff5c or fastmul5 f350aa62), every run
# with HP_EXACT_RECIP=1 (the default from 33eeff5c): D 300 u base and halved steps, D 300 Moebius base, D 1000 base and
# halved steps, D 1000 at M 48; each by release_ls --harm 13 --kmax 13 from the state (at M 48: --harm 13,15,...,23
# --kmax 31) with the qq Jacobian for h13 (h13 at D 300 handed over to qq anyway), the octo-double residual, tol 1e-48.
# Usage: fix_reruns.sh RAW OUT SITE THREADS [RELAXED]   (RAW: the raw clone; OUT: a task folder in it)
{
RAW=$1; O=$2; SITE=$3; T=$4; REL=${5:-0}
cd "$(dirname "$0")/hp" 2>/dev/null || cd hp || exit 1
grep -q 'def exact_recip' form_s.py || exit 1
PY=${PYTHON:-python3}
export HP_EXACT_RECIP=1 OPENBLAS_NUM_THREADS=1
[ "$REL" = 1 ] && export HP_HORIZON_RELAXED=1
mkdir -p $O
run() {  # name state extra-args
  mkdir -p $O/$1
  date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/$1/run.log
  PYTHONPATH=$SITE $PY -u form_s.py release_ls $2 $O/$1 $3 --res od --tol 1e-48 --tol_h 1e-44 --threads $T --outer 8 \
    --commit 33eeff5c > $O/$1/rls.log 2>&1
  echo "rc $?" >> $O/$1/run.log
  date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/$1/run.log
}
run D300_u_base $RAW/I1098-dh610/budget300_src/D300_full_base.npz "--harm 13 --kmax 13 --jac_by 13:qq" &
run D300_u_steps2 $RAW/I1098-mac-a/budget300_src/D300_full_steps2.npz "--harm 13 --kmax 13 --jac_by 13:qq" &
run D300_mob_base "$RAW/I1098-dh610/budget300_src/D300_full_mob8,ks=600.npz" "--harm 13 --kmax 13 --jac_by 13:qq" &
wait
run D1000_base $RAW/I1098-dh610/budget1000_src/D1000_full_base.npz "--harm 13 --kmax 13 --jac_by 13:qq" &
run D1000_steps2 $RAW/I1098-dh610/budget1000_src/D1000_full_steps2.npz "--harm 13 --kmax 13 --jac_by 13:qq" &
wait
exit
}
