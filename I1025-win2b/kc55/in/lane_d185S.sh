#!/bin/bash
{
# #1025 D 18.5 (the coordinator's ruling after (A), d18_criteria.log): after lane_d185L.sh reaches D 18.5, the hybrid sign scan
# over lambda 1.55-1.90 at 0.01 (d18_hybsign.py, noise test, float64 beside) on the leap's state and record, then its reading
# (d185_scan_read.py, against D 18's scan and bisected lower root). usage: lane_d185S.sh WAIT_PID [dry]
set -u
WAIT=$1; MODE=${2:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter; TAG=l1kc63Wm1025
ST=$Q/sol_${TAG}_D18.5000.npy; REC=$Q/$TAG.jsonl; SCAN=$Q/d185_scan_1025.jsonl; REF=$Q/d18_scan_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" "$REF ac80e9d5bd9c42b1ff10eea65d26258b3314021f"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py \
  || { say "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $SCAN $Q/d185_scan.log $Q/d185_scan_read.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d185_scan_read 7c9d400fd0966a35ac306b5495febb4ec4efe7da, D 18 scan ac80e9d5bd9c42b1ff10eea65d26258b3314021f, solver code = 505d8399, ell_delta = 48c36355; waiting for pid $WAIT"
[ "$MODE" = dry ] && exit 0
while kill -0 $WAIT 2> /dev/null; do sleep 60; done
say "pid $WAIT has exited"
grep -q '^== .* lane d185L done' $Q/lane_d185L.log && [ -f $ST ] && [ -f $REC ] || { say "STOP: the leap did not reach D 18.5 (lane_d185L.log)"; exit; }
grep -E '^== .* state ' $Q/lane_d185L.log
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(36)))')
say "scan: the hybrid at $L (timeout 21600 s)"
cd $W
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scan.log
r=${PIPESTATUS[0]}; say "scan exit $r"
[ $r = 0 ] || { say "STOP: the scan did not finish (exit $r; 3 = not the record system)"; exit; }
$PY $Q/d185_scan_read.py $SCAN 18.5 $W $REF 1.7749781027 - > $Q/d185_scan_read.log 2>&1; r=$?
cat $Q/d185_scan_read.log; say "reader exit $r"
say "lane d185S done"
exit
}
