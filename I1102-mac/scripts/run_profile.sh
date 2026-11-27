#!/bin/bash
# #1102: profile one ellrs evaluation at k_c 55 and 87 (T threads, 6 by default), beside one DDEll stage in Python;
# usage: run_profile.sh SITE MATTER_DIR [T] [TAG] (TAG names the logs, profile_kc<k_c>_t<T>_<TAG>.log)
{
R=$(cd "$(dirname "$0")/.." && pwd)
SITE=$1; MATTER=$2; T=${3:-6}; TAG=${4:+_$4}
cd "$R"
while read -r stub st D lam kc; do
  VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE OMP_NUM_THREADS=1 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u scripts/profile_b12.py "$MATTER" in/$stub in/$st $D $lam $T \
    --out=profile/profile.jsonl > profile/profile_kc${kc}_t$T$TAG.log 2>&1
done <<'LIST'
l1kc55F1025.jsonl sol_l1kc55F1025_D18.125000.npy 18.125 1.775 55
l1kc87Ldh370.jsonl sol_l1kc87Ldh370_D21.062500.npy 21.0625 0.895 87
LIST
exit
}
