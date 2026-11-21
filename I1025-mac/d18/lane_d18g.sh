#!/bin/bash
{
# #1025 (g) (d18_criteria.log, the coordinator's ruling after (e)): D 18.25 over 2.25-2.60 at 0.05, then 0.01 inside each bracket with a
# sign change, read by d18f_read.py window (a robust change places the upper root). usage: lane_d18g.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC=$Q/l1kc63Wm1025.jsonl; ST25=$Q/sol_l1kc63Wm1025_D18.250000.npy; REF=$Q/d18_refsign_1025.jsonl; UP25=$Q/d1825_scanup_1025.jsonl
HI=$Q/d1825_hi_1025.jsonl; HIF=$Q/d1825_hifine_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18f_read.py 5fb96dceb427e965b830b42db5b8f30255f20532" \
          "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$REC 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" \
          "$ST25 eae8ca0212bd7e9cad6f1fc92da1b88541fbd8f5" "$REF 3e2d8b4e8f72943983fab091730629464b04e854" "$UP25 c443fcbaccf1f57ad7316d0e23a66b753b78997a"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $HI $HIF $Q/d1825_hi.log $Q/d1825_hifine.log $Q/d1825_hi_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18f_read 5fb96dce, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, record 08f4dbf3, state eae8ca02, refsign 3e2d8b4e, (e) scan c443fcba; solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
cd $W
hyb() { timeout $1 nice -n 10 $PY -u $Q/d18_hybsign.py $2 $3 $4 $5 $6 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' >> $7; return ${PIPESTATUS[0]}; }
L=$($PY -c 'print(",".join(f"{2.25 + 0.05 * i:.2f}" for i in range(8)))')
say "(g) D 18.25: the hybrid at $L (timeout 5400 s)"
hyb 5400 $REC $ST25 18.25 $L $HI $Q/d1825_hi.log; r=$?; say "(g) coarse exit $r"
[ $r = 0 ] || { say "STOP: (g) coarse did not finish (exit $r)"; exit; }
P=$($PY $Q/d18f_read.py refine 18.25 2.25 2.60 $REF,$UP25,$HI 2>&1); r=$?
[ $r = 0 ] || { say "STOP: (g) refine: $P (exit $r); the coordinator rules"; exit; }
say "(g) D 18.25 inside the brackets: the hybrid at $P (timeout 5400 s)"
hyb 5400 $REC $ST25 18.25 $P $HIF $Q/d1825_hifine.log; r=$?; say "(g) fine exit $r"
[ $r = 0 ] || { say "STOP: (g) fine did not finish (exit $r)"; exit; }
cat $Q/d1825_hi.log $Q/d1825_hifine.log
$PY $Q/d18f_read.py window 18.25 2.25 2.60 $REF,$UP25,$HI,$HIF 2>&1 | grep -v Warning > $Q/d1825_hi_read.log; r=${PIPESTATUS[0]}
cat $Q/d1825_hi_read.log; say "(g) reader exit $r"
say "lane d18g done"
exit
}
