#!/bin/bash
{
# #1025 the k_c 63 leap D 18 -> 18.5 (the coordinator's ruling after (A), d18_criteria.log): winb's flags, h 0.0625, seeds winb's
# D 17.9375 and D 18 states, 12 h cap; then the record and the D 18.5 state are copied into d18/. usage: lane_d185L.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter; TAG=l1kc63Wm1025
SA=$Q/sol_l1kc63W1025_D17.937500.npy; SB=$Q/sol_l1kc63W1025_D18.000000.npy
LJ=$W/data/$TAG.jsonl; ST=$Q/sol_${TAG}_D18.5000.npy; LOG=$Q/leap_kc63_d185.log
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$W/ell_leap.py 1eb873e49348f400d9d0dfc1cd95be5761473d0c" "$SA a8f78f18fed4ea395aa025dc12ec3009ceb7c92b" \
          "$SB 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_leap.py \
  solver/matter/ddnp.py || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $LJ $ST $LOG $Q/$TAG.jsonl; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: ell_leap 1eb873e4, seeds a8f78f18 (D 17.9375) and 45e72c6a (D 18), solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
say "leap: ell_leap.py $TAG 1 63 D 17.9375, 18 -> 18.5, h 0.0625 (timeout 43200 s)"
cd $W
timeout 43200 nice -n 10 $PY -u ell_leap.py $TAG 1 63 $SA 17.9375 $SB 18 18.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold \
  < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  ' > $LOG
rc=${PIPESTATUS[0]}
say "leap exit $rc"
tail -n 2 $LOG | cut -c1-200
cp $LJ $Q/ 2> /dev/null
[ $rc = 0 ] && grep -q '^reached D 18.5' $LOG && [ -f $W/data/sol_${TAG}_D18.5000.npy ] \
  || { say "STOP: the leap did not reach D 18.5"; exit; }
cp $W/data/sol_${TAG}_D18.5000.npy $ST
say "state $(basename $ST) blob $(hb $ST); record $(basename $LJ) blob $(hb $Q/$TAG.jsonl)"
say "lane d185L done"
exit
}
