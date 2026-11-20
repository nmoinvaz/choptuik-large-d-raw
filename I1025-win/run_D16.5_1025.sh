#!/bin/bash
# #1025 (win), the coordinator's job: k_c 63 lambda at D 16.5 from the Mac's k_c 55 state (hash 557bfff0 checked), 4 BLAS threads, 12 h timeout
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') ell_refine.py l1kc55Fb1025 55 l1kc63Fw1025b 63 1 16.5 2.159124821824751 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60" >> $LOGS/kc63_D16.5.log
timeout 43200 "$PY" -u ell_refine.py l1kc55Fb1025 55 l1kc63Fw1025b 63 1 16.5 2.159124821824751 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $LOGS/kc63_D16.5.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/kc63_D16.5.log
