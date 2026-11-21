#!/bin/bash
{
# #1025 (d18_criteria.log, the coordinator's rulings after the sign-convention check), one process at a time: (iii) lambda 1.20 on the
# leap's D 18.3125, 18.375, 18.4375; (ii) D 18.25 over 1.20-1.55 at 0.05, then 0.01 inside each bracket; (i) (e) as queued, D 18.5 over
# 2.10-2.40 and D 18.25 over 1.95-2.25. usage: lane_d18f.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC=$Q/l1kc63Wm1025.jsonl; ST25=$Q/sol_l1kc63Wm1025_D18.250000.npy; ST185=$Q/sol_l1kc63Wm1025_D18.5000.npy; REF=$Q/d18_refsign_1025.jsonl
III=$Q/d18f_iii_1025.jsonl; LOW=$Q/d1825_low_1025.jsonl; LOWF=$Q/d1825_lowfine_1025.jsonl
UP185=$Q/d185_scanup_1025.jsonl; UP25=$Q/d1825_scanup_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18f_read.py 5fb96dceb427e965b830b42db5b8f30255f20532" \
          "$Q/d18e_read.py 24ef65985571aa6ec1599b1dd2cfa845ed101eeb" "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" \
          "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" \
          "$REC 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" "$ST25 eae8ca0212bd7e9cad6f1fc92da1b88541fbd8f5" "$ST185 33c1a58b82229d55661cbd5e79d2c1fce0c0717c" \
          "$Q/sol_l1kc63Wm1025_D18.312500.npy d8bbd43b22fc6440dfd391b73e023a657a929cd8" "$Q/sol_l1kc63Wm1025_D18.375000.npy aa04459266643be3dfd46c2d83c52f556ed6254c" \
          "$Q/sol_l1kc63Wm1025_D18.437500.npy 16a17e5f6c93ffc425c71e1e2d9a2cab42c4827d" "$REF 3e2d8b4e8f72943983fab091730629464b04e854" \
          "$Q/d1825_scan_1025.jsonl a66a2a4aa60c24d26382397409e949f69aeda9cb" "$Q/d185_scan_1025.jsonl 90540dafdae9ff4093240cdc79d3ef8cc0506000" \
          "$Q/d185_scanhi_1025.jsonl 496f4b6396a03fee0b7558f4e10a7b723e68bcf1"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py \
  || { say "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $III $LOW $LOWF $UP185 $UP25 $Q/d18f_iii.log $Q/d18f_iii_read.log $Q/d1825_low.log $Q/d1825_lowfine.log $Q/d1825_low_read.log \
         $Q/d185_scanup.log $Q/d1825_scanup.log $Q/d185_e_read.log $Q/d1825_e_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18f_read 5fb96dce, d18e_read 24ef6598, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, record 08f4dbf3, states eae8ca02, 33c1a58b, d8bbd43b, aa044592, 16a17e5f, refsign 3e2d8b4e, scans a66a2a4a, 90540daf, 496f4b63; solver code = 505d8399, ell_delta = 48c36355"
[ "$MODE" = dry ] && exit 0
cd $W
hyb() { timeout $1 nice -n 10 $PY -u $Q/d18_hybsign.py $2 $3 $4 $5 $6 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' >> $7; return ${PIPESTATUS[0]}; }
for d in 18.3125:18.312500 18.375:18.375000 18.4375:18.437500; do
  say "(iii) D ${d%%:*}: the hybrid at 1.20 (timeout 900 s)"
  hyb 900 $REC $Q/sol_l1kc63Wm1025_D${d#*:}.npy ${d%%:*} 1.20 $III $Q/d18f_iii.log; r=$?; say "(iii) D ${d%%:*} exit $r"
  [ $r = 0 ] || { say "STOP: (iii) D ${d%%:*} did not finish (exit $r; 3 = not the record system)"; exit; }
done
cat $Q/d18f_iii.log
$PY $Q/d18f_read.py dseq 1.2 $REF,$III > $Q/d18f_iii_read.log 2>&1; r=$?; cat $Q/d18f_iii_read.log; say "(iii) reader exit $r"
say "(iii) done"
L=$($PY -c 'print(",".join(f"{1.20 + 0.05 * i:.2f}" for i in range(8)))')
say "(ii) D 18.25: the hybrid at $L (timeout 3600 s)"
hyb 3600 $REC $ST25 18.25 $L $LOW $Q/d1825_low.log; r=$?; say "(ii) coarse exit $r"
[ $r = 0 ] || { say "STOP: (ii) coarse did not finish (exit $r)"; exit; }
P=$($PY $Q/d18f_read.py refine 18.25 1.20 1.55 $REF,$Q/d1825_scan_1025.jsonl,$LOW 2>&1); r=$?
[ $r = 0 ] || { say "STOP: (ii) refine: $P (exit $r); the coordinator rules"; exit; }
say "(ii) D 18.25 inside the brackets: the hybrid at $P (timeout 3600 s)"
hyb 3600 $REC $ST25 18.25 $P $LOWF $Q/d1825_lowfine.log; r=$?; say "(ii) fine exit $r"
[ $r = 0 ] || { say "STOP: (ii) fine did not finish (exit $r)"; exit; }
cat $Q/d1825_low.log $Q/d1825_lowfine.log
$PY $Q/d18f_read.py window 18.25 1.20 1.55 $REF,$Q/d1825_scan_1025.jsonl,$LOW,$LOWF 2>&1 | grep -v Warning > $Q/d1825_low_read.log; r=${PIPESTATUS[0]}
cat $Q/d1825_low_read.log; say "(ii) reader exit $r"
say "(ii) done"
L=$($PY -c 'print(",".join(f"{2.10 + 0.01 * i:.2f}" for i in range(31)))')
say "(e) D 18.5: the hybrid at $L (timeout 10800 s)"
hyb 10800 $REC $ST185 18.5 $L $UP185 $Q/d185_scanup.log; r=$?; say "(e) D 18.5 scan exit $r"
[ $r = 0 ] || { say "STOP: the (e) D 18.5 scan did not finish (exit $r)"; exit; }
$PY $Q/d18e_read.py 18.5 $W $Q/d185_scan_1025.jsonl,$Q/d185_scanhi_1025.jsonl,$UP185 2.10 2.40 2>&1 | grep -v Warning > $Q/d185_e_read.log; r=${PIPESTATUS[0]}
cat $Q/d185_e_read.log; say "(e) D 18.5 reader exit $r"
say "(e) D 18.5 done"
L=$($PY -c 'print(",".join(f"{1.95 + 0.01 * i:.2f}" for i in range(31)))')
say "(e) D 18.25: the hybrid at $L (timeout 10800 s)"
hyb 10800 $REC $ST25 18.25 $L $UP25 $Q/d1825_scanup.log; r=$?; say "(e) D 18.25 scan exit $r"
[ $r = 0 ] || { say "STOP: the (e) D 18.25 scan did not finish (exit $r)"; exit; }
$PY $Q/d18e_read.py 18.25 $W $Q/d1825_scan_1025.jsonl,$UP25 1.95 2.25 2>&1 | grep -v Warning > $Q/d1825_e_read.log; r=${PIPESTATUS[0]}
cat $Q/d1825_e_read.log; say "(e) D 18.25 reader exit $r"
say "lane d18f done"
exit
}
