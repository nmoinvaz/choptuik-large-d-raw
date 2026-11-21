#!/bin/bash
{
# #1025 (k) (d18_criteria.log, the coordinator's next task): D 17.75 at k_c 55, the hybrid over 1.65-1.90 at 0.01 on the Mac's state and
# record line, read against k_c 63 at D 17.75 (dh170's scans) by d18k_read.py. usage: lane_d18k.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; O=$R/out; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC=$O/l1kc55F1025.jsonl; ST=$O/sol_l1kc55F1025_D17.750000.npy; OUT=$Q/d1775k55_scan_1025.jsonl
K63=$Q/dh170_d1775_scan_copy.jsonl,$Q/dh170_d1775b_scan_copy.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18k_read.py 15c62ca5c26e16d8f4d4971c5b197d7680d23bff" \
          "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$REC 0fb77df8281d634e6ecf2d3b2038e3706df3c960" \
          "$ST c19c23abd5279bf72ed03d57e7ca0e1d42fd0420" "$Q/dh170_d1775_scan_copy.jsonl 7844dcc8ddd882961a1000ecfcf4fff3849b52d4" \
          "$Q/dh170_d1775b_scan_copy.jsonl 30d7c5a973bd78feeaaa003fa04ee3df6610a3a5"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $OUT $Q/d1775k55_scan.log $Q/d1775k55_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18k_read 15c62ca5, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, record 0fb77df8, state c19c23ab, k_c 63 copies 7844dcc8, 30d7c5a9; solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
cd $W
L=$($PY -c 'print(",".join(f"{1.65 + 0.01 * i:.2f}" for i in range(26)))')
say "(k) D 17.75 k_c 55: the hybrid at $L (timeout 14400 s)"
timeout 14400 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 17.75 $L $OUT < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d1775k55_scan.log
r=${PIPESTATUS[0]}; say "(k) scan exit $r"
[ $r = 0 ] || { say "STOP: the (k) scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18k_read.py 17.75 1.65 1.90 $OUT $K63 2>&1 | grep -v Warning > $Q/d1775k55_read.log; r=${PIPESTATUS[0]}
cat $Q/d1775k55_read.log; say "(k) reader exit $r"
say "lane d18k done"
exit
}
