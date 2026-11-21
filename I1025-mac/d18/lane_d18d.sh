#!/bin/bash
{
# #1025 (d) (d18_criteria.log, the coordinator's input after (a)): after lane_d18c.sh, the D 18.5 hybrid scan over 1.90-2.10 on the
# leap's state, then the D 18 scan over 1.90-2.10 on winb's state, then every root with its orientation at D 18, 18.25 and 18.5
# (d18d_read.py). usage: lane_d18d.sh WAIT_PID [dry]
set -u
WAIT=$1; MODE=${2:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
ST18=$Q/sol_l1kc63W1025_D18.000000.npy; STUB18=$Q/d18_stub_l1kc63W1025.jsonl
ST185=$Q/sol_l1kc63Wm1025_D18.5000.npy; REC=$Q/l1kc63Wm1025.jsonl
HI185=$Q/d185_scanhi_1025.jsonl; HI18=$Q/d18_scanhi_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18d_read.py 6b6089034738a45c8dc9e6831a1654c1bac4ed18" \
          "$Q/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" \
          "$ST18 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$STUB18 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" \
          "$ST185 33c1a58b82229d55661cbd5e79d2c1fce0c0717c" "$REC 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" \
          "$Q/d185_scan_1025.jsonl 90540dafdae9ff4093240cdc79d3ef8cc0506000" "$Q/d18_scan_1025.jsonl ac80e9d5bd9c42b1ff10eea65d26258b3314021f" \
          "$Q/d18_scanlow_1025.jsonl c6475497c46493fee1d02c38cd7c3b0ad865e7d3"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py \
  || { say "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $HI185 $HI18 $Q/d185_scanhi.log $Q/d18_scanhi.log $Q/d185_d_read.log $Q/d18_d_read.log $Q/d1825_d_read.log; do
  [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18d_read 6b608903, d18c_read 1383470f, d185_scan_read 7c9d400f, states 45e72c6a (D 18) and 33c1a58b (D 18.5), stub 2cfdb833, record 08f4dbf3, scans 90540daf, ac80e9d5, c6475497; waiting for pid $WAIT"
[ "$MODE" = dry ] && exit 0
while kill -0 $WAIT 2> /dev/null; do sleep 60; done
say "pid $WAIT has exited"; grep -E '^== .* (lane d18c done|STOP)' $Q/lane_d18c.log
cd $W
L=$($PY -c 'print(",".join(f"{1.90 + 0.01 * i:.2f}" for i in range(21)))')
say "(d) D 18.5: the hybrid at $L (timeout 7200 s)"
timeout 7200 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST185 18.5 $L $HI185 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scanhi.log
r=${PIPESTATUS[0]}; say "(d) D 18.5 scan exit $r"
[ $r = 0 ] || { say "STOP: the D 18.5 scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18d_read.py 18.5 $W $Q/d185_scan_1025.jsonl,$HI185 --above=1.90 > $Q/d185_d_read.log 2>&1; r=$?
cat $Q/d185_d_read.log; say "(d) D 18.5 reader exit $r"
say "(d) D 18.5 done"
say "(d) D 18: the hybrid at $L (timeout 7200 s)"
timeout 7200 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB18 $ST18 18 $L $HI18 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_scanhi.log
r=${PIPESTATUS[0]}; say "(d) D 18 scan exit $r"
[ $r = 0 ] || { say "STOP: the D 18 scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d18d_read.py 18 $W $Q/d18_scanlow_1025.jsonl,$Q/d18_scan_1025.jsonl,$HI18 > $Q/d18_d_read.log 2>&1; r=$?
cat $Q/d18_d_read.log; say "(d) D 18 reader exit $r"
if [ -s $Q/d1825_scan_1025.jsonl ]; then
  $PY $Q/d18d_read.py 18.25 $W $Q/d1825_scan_1025.jsonl > $Q/d1825_d_read.log 2>&1; r=$?
  cat $Q/d1825_d_read.log; say "(d) D 18.25 orientations, reader exit $r"
fi
say "lane d18d done"
exit
}
