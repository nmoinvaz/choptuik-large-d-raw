#!/bin/bash
{
# #1025 (e) (d18_criteria.log, the coordinator's ruling after (d)): after lane_d18r.sh, d18_refsign_steps.py (the flips beside the step
# changes); then, ONLY if the sign-convention check reads that the convention holds, the D 18.5 hybrid scan over 2.10-2.40 and the
# D 18.25 scan over 1.95-2.25, each read by d18e_read.py. Any other verdict stops the lane. usage: lane_d18e.sh WAIT_PID [dry]
set -u
WAIT=$1; MODE=${2:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
REC=$Q/l1kc63Wm1025.jsonl; ST185=$Q/sol_l1kc63Wm1025_D18.5000.npy; ST25=$Q/sol_l1kc63Wm1025_D18.250000.npy
UP185=$Q/d185_scanup_1025.jsonl; UP25=$Q/d1825_scanup_1025.jsonl
STEPS="$Q/winb_l1kc63W1025_copy.jsonl:$Q/sol_l1kc63W1025_D17.750000.npy:17.75,$Q/d18_stub_l1kc63W1025.jsonl:$Q/sol_l1kc63W1025_D18.000000.npy:18"
for d in 18.0625:18.062500 18.125:18.125000 18.1875:18.187500 18.25:18.250000; do STEPS="$STEPS,$REC:$Q/sol_l1kc63Wm1025_D${d#*:}.npy:${d%%:*}"; done
STEPS="$STEPS,$REC:$ST185:18.5"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18e_read.py 24ef65985571aa6ec1599b1dd2cfa845ed101eeb" \
          "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" \
          "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$Q/d18_refsign_steps.py d5b1e50a821429b4e2e6f9f6963a000037144e04" \
          "$Q/d18_refsign_read.py 6ae9035ef9e1144f615fdeb633bc2d6987f9dcbe" "$REC 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" \
          "$ST185 33c1a58b82229d55661cbd5e79d2c1fce0c0717c" "$ST25 eae8ca0212bd7e9cad6f1fc92da1b88541fbd8f5" \
          "$Q/d185_scan_1025.jsonl 90540dafdae9ff4093240cdc79d3ef8cc0506000" "$Q/d185_scanhi_1025.jsonl 496f4b6396a03fee0b7558f4e10a7b723e68bcf1" \
          "$Q/d1825_scan_1025.jsonl a66a2a4aa60c24d26382397409e949f69aeda9cb"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py \
  || { say "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $UP185 $UP25 $Q/d185_scanup.log $Q/d1825_scanup.log $Q/d185_e_read.log $Q/d1825_e_read.log $Q/d18_refsign_steps.log; do
  [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18e_read 24ef6598, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, d18_refsign_steps d5b1e50a, d18_refsign_read 6ae9035e, record 08f4dbf3, states 33c1a58b (D 18.5) and eae8ca02 (D 18.25), scans 90540daf, 496f4b63, a66a2a4a; solver code = 505d8399, ell_delta = 48c36355; waiting for pid $WAIT"
[ "$MODE" = dry ] && exit 0
while kill -0 $WAIT 2> /dev/null; do sleep 60; done
say "pid $WAIT has exited"; grep -E '^== .* (lane d18r done|STOP)' $Q/lane_d18r.log
grep -qE '^== .* lane d18r done' $Q/lane_d18r.log || { say "STOP: the sign-convention check did not finish; (e) does not run"; exit; }
$PY $Q/d18_refsign_steps.py $Q/d18_refsign_1025.jsonl "$STEPS" 2>&1 | grep -v Warning > $Q/d18_refsign_steps.log; r=${PIPESTATUS[0]}
cat $Q/d18_refsign_steps.log; say "d18_refsign_steps exit $r"
if ! grep -q '^reading: both reference signs are constant across D; the convention holds' $Q/d18_refsign_read.log; then
  grep -E '^(reading|no reading|no convention reading|missing)' $Q/d18_refsign_read.log
  say "STOP: the sign-convention check does not read that the convention holds; (e) does not run, the coordinator rules"; exit
fi
say "the convention holds (d18_refsign_read.log); (e) runs"
cd $W
L=$($PY -c 'print(",".join(f"{2.10 + 0.01 * i:.2f}" for i in range(31)))')
say "(e) D 18.5: the hybrid at $L (timeout 10800 s)"
timeout 10800 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST185 18.5 $L $UP185 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scanup.log
r=${PIPESTATUS[0]}; say "(e) D 18.5 scan exit $r"
[ $r = 0 ] || { say "STOP: the D 18.5 scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18e_read.py 18.5 $W $Q/d185_scan_1025.jsonl,$Q/d185_scanhi_1025.jsonl,$UP185 2.10 2.40 2>&1 | grep -v Warning > $Q/d185_e_read.log; r=${PIPESTATUS[0]}
cat $Q/d185_e_read.log; say "(e) D 18.5 reader exit $r"
say "(e) D 18.5 done"
L=$($PY -c 'print(",".join(f"{1.95 + 0.01 * i:.2f}" for i in range(31)))')
say "(e) D 18.25: the hybrid at $L (timeout 10800 s)"
timeout 10800 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST25 18.25 $L $UP25 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d1825_scanup.log
r=${PIPESTATUS[0]}; say "(e) D 18.25 scan exit $r"
[ $r = 0 ] || { say "STOP: the D 18.25 scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18e_read.py 18.25 $W $Q/d1825_scan_1025.jsonl,$UP25 1.95 2.25 2>&1 | grep -v Warning > $Q/d1825_e_read.log; r=${PIPESTATUS[0]}
cat $Q/d1825_e_read.log; say "(e) D 18.25 reader exit $r"
say "lane d18e done"
exit
}
