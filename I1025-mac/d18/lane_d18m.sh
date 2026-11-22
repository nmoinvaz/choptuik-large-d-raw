#!/bin/bash
{
# #1025 (m) (d18_criteria.log, the coordinator's next task): D 18.125 at k_c 55, the hybrid over 1.65-1.90 at 0.01 on the Mac's state and
# record line, read against k_c 63 at D 18.125 (winb's scan) by d18k2_read.py. usage: lane_d18m.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; O=$R/out; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC=$O/l1kc55F1025.jsonl; ST=$O/sol_l1kc55F1025_D18.125000.npy; OUT=$Q/d18125k55_scan_1025.jsonl; K63=$Q/winb_d18mid_scan_copy.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18k2_read.py 52f31e5355d642f667c6bc263004644ae645e072" \
          "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$REC 0fb77df8281d634e6ecf2d3b2038e3706df3c960" \
          "$ST 88ccda5c9bc80f95905fa1bf1180bd31b9193ac5" "$K63 6b7a4aa525c6c1efed1827d065e20538f285022c"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $OUT $Q/d18125k55_scan.log $Q/d18125k55_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18k2_read 52f31e53, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, record 0fb77df8, state 88ccda5c, k_c 63 copy 6b7a4aa5; solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
cd $W
L=$($PY -c 'print(",".join(f"{1.65 + 0.01 * i:.2f}" for i in range(26)))')
say "(m) D 18.125 k_c 55: the hybrid at $L (timeout 14400 s)"
timeout 14400 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.125 $L $OUT < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18125k55_scan.log
r=${PIPESTATUS[0]}; say "(m) scan exit $r"
[ $r = 0 ] || { say "STOP: the (m) scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18k2_read.py 18.125 1.65 1.90 $OUT $K63 2>&1 | grep -v Warning > $Q/d18125k55_read.log; r=${PIPESTATUS[0]}
cat $Q/d18125k55_read.log; say "(m) reader exit $r"
say "lane d18m done"
exit
}
