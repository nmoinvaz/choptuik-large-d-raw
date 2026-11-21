#!/bin/bash
{
# #1025 (a) then (b) (d18_criteria.log, the coordinator's ruling after the D 18.5 scan): (a) the D 18 hybrid scan over 1.55-1.69
# on winb's state, read with (A)'s 1.70-1.90; (b) the D 18.25 hybrid scan over 1.55-1.95 on the leap's state. usage: lane_d18c.sh [dry]
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
ST18=$Q/sol_l1kc63W1025_D18.000000.npy; STUB18=$Q/d18_stub_l1kc63W1025.jsonl; A18=$Q/d18_scan_1025.jsonl; LOW=$Q/d18_scanlow_1025.jsonl
ST25=$Q/sol_l1kc63Wm1025_D18.250000.npy; REC=$Q/l1kc63Wm1025.jsonl; S25=$Q/d1825_scan_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$ST18 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" \
          "$STUB18 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" "$A18 ac80e9d5bd9c42b1ff10eea65d26258b3314021f" \
          "$ST25 eae8ca0212bd7e9cad6f1fc92da1b88541fbd8f5" "$REC 08f4dbf367edba55814e5cf989ccd32a9a5dbe67"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py \
  || { say "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $LOW $S25 $Q/d18_scanlow.log $Q/d18c_a_read.log $Q/d1825_scan.log $Q/d1825_scan_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18c_read 1383470f, d185_scan_read 7c9d400f, D 18 state 45e72c6a and stub 2cfdb833, (A) ac80e9d5, D 18.25 state eae8ca02, leap record 08f4dbf3, solver code = 505d8399, ell_delta = 48c36355"
[ "$MODE" = dry ] && exit 0
cd $W
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(15)))')
say "(a): the D 18 hybrid at $L (timeout 7200 s)"
timeout 7200 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB18 $ST18 18 $L $LOW < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_scanlow.log
r=${PIPESTATUS[0]}; say "(a) scan exit $r"
[ $r = 0 ] || { say "STOP: the (a) scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18c_read.py a 18 $W $LOW,$A18 > $Q/d18c_a_read.log 2>&1; r=$?
cat $Q/d18c_a_read.log; say "(a) reader exit $r"
say "(a) done"
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(41)))')
say "(b): the D 18.25 hybrid at $L (timeout 21600 s)"
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST25 18.25 $L $S25 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d1825_scan.log
r=${PIPESTATUS[0]}; say "(b) scan exit $r"
[ $r = 0 ] || { say "STOP: the (b) scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18c_read.py b 18.25 $W $S25 > $Q/d1825_scan_read.log 2>&1; r=$?
cat $Q/d1825_scan_read.log; say "(b) reader exit $r"
say "lane d18c done"
exit
}
