#!/bin/bash
{
# #1025 kc_break (README.md, the coordinator's task): D 18.3125, the hybrid over 1.62-1.80 at 0.01 at k_c 63 and k_c 55 side by side,
# 4 BLAS threads each, nice 10, 8 h caps; then d18k2_read.py. usage: lane_kcb.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; K=$R/kc_break; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC63=$Q/l1kc63Wm1025.jsonl; ST63=$Q/sol_l1kc63Wm1025_D18.312500.npy; REC55=$R/out/l1kc55F1025.jsonl; ST55=$R/out/sol_l1kc55F1025_D18.312500.npy
O63=$K/kcb_k63_1025.jsonl; O55=$K/kcb_k55_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18k2_read.py 52f31e5355d642f667c6bc263004644ae645e072" \
          "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$REC63 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" \
          "$ST63 d8bbd43b22fc6440dfd391b73e023a657a929cd8" "$REC55 0fb77df8281d634e6ecf2d3b2038e3706df3c960" \
          "$ST55 3ee23e868fdf7936535385ce3043e1ffc086be14"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $O63 $O55 $K/kcb_k63.log $K/kcb_k55.log $K/kcb_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18k2_read 52f31e53, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, k_c 63 state d8bbd43b and record 08f4dbf3, k_c 55 state 3ee23e86 and record 0fb77df8; solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
cd $W
L=$($PY -c 'print(",".join(f"{1.62 + 0.01 * i:.2f}" for i in range(19)))')
say "D 18.3125 at k_c 63 and k_c 55 side by side: the hybrid at $L (timeout 28800 s each)"
( timeout 28800 nice -n 10 $PY -u $Q/d18_hybsign.py $REC63 $ST63 18.3125 $L $O63 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $K/kcb_k63.log; exit ${PIPESTATUS[0]} ) &
p63=$!
( timeout 28800 nice -n 10 $PY -u $Q/d18_hybsign.py $REC55 $ST55 18.3125 $L $O55 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $K/kcb_k55.log; exit ${PIPESTATUS[0]} ) &
p55=$!
wait $p63; r63=$?; say "k_c 63 scan exit $r63"
wait $p55; r55=$?; say "k_c 55 scan exit $r55"
[ $r63 = 0 ] && [ $r55 = 0 ] || { say "STOP: a scan did not finish (k_c 63 exit $r63, k_c 55 exit $r55; 3 = not the record system)"; exit; }
$PY $Q/d18k2_read.py 18.3125 1.62 1.80 $O55 $O63 2>&1 | grep -v Warning > $K/kcb_read.log; r=${PIPESTATUS[0]}
cat $K/kcb_read.log; say "reader exit $r"
say "lane kcb done"
exit
}
