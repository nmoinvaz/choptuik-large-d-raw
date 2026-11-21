#!/bin/bash
{
# #1025, the coordinator's check of det's sign convention across the k_c 63 states (d18_criteria.log, after (b)'s ruling): after
# lane_d18d.sh, the hybrid sign at lambda 1.20 and 2.60 with the noise test on each state at D 17.75, 18, 18.0625, 18.125, 18.1875,
# 18.25 and 18.5, then d18_refsign_read.py. usage: lane_d18r.sh WAIT_PID [dry]
set -u
WAIT=$1; MODE=${2:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
OUT=$Q/d18_refsign_1025.jsonl; LOG=$Q/d18_refsign.log; RD=$Q/d18_refsign_read.log
RUNS=("$Q/winb_l1kc63W1025_copy.jsonl $Q/sol_l1kc63W1025_D17.750000.npy 17.75"
      "$Q/d18_stub_l1kc63W1025.jsonl $Q/sol_l1kc63W1025_D18.000000.npy 18"
      "$Q/l1kc63Wm1025.jsonl $Q/sol_l1kc63Wm1025_D18.062500.npy 18.0625"
      "$Q/l1kc63Wm1025.jsonl $Q/sol_l1kc63Wm1025_D18.125000.npy 18.125"
      "$Q/l1kc63Wm1025.jsonl $Q/sol_l1kc63Wm1025_D18.187500.npy 18.1875"
      "$Q/l1kc63Wm1025.jsonl $Q/sol_l1kc63Wm1025_D18.250000.npy 18.25"
      "$Q/l1kc63Wm1025.jsonl $Q/sol_l1kc63Wm1025_D18.5000.npy 18.5")
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18_refsign_read.py 6ae9035ef9e1144f615fdeb633bc2d6987f9dcbe" \
          "$Q/winb_l1kc63W1025_copy.jsonl c33039dfa38b495486fb3ef7da77077d43db775a" "$Q/d18_stub_l1kc63W1025.jsonl 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" \
          "$Q/l1kc63Wm1025.jsonl 08f4dbf367edba55814e5cf989ccd32a9a5dbe67" \
          "$Q/sol_l1kc63W1025_D17.750000.npy de9fc3e55aa46bafd4ef62536861f94aed9e3035" "$Q/sol_l1kc63W1025_D18.000000.npy 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" \
          "$Q/sol_l1kc63Wm1025_D18.062500.npy f2307f0e8ffb4621b61f74450a920c652981d973" "$Q/sol_l1kc63Wm1025_D18.125000.npy 5bf7b711a2dbbabb664201e182f90b79d88bb037" \
          "$Q/sol_l1kc63Wm1025_D18.187500.npy 3f06b92e088953cf0d844b07a9a041be520480ff" "$Q/sol_l1kc63Wm1025_D18.250000.npy eae8ca0212bd7e9cad6f1fc92da1b88541fbd8f5" \
          "$Q/sol_l1kc63Wm1025_D18.5000.npy 33c1a58b82229d55661cbd5e79d2c1fce0c0717c"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $OUT $LOG $RD; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: d18_hybsign e089207a, d18_refsign_read 6ae9035e, records c33039df, 2cfdb833, 08f4dbf3, states de9fc3e5, 45e72c6a, f2307f0e, 5bf7b711, 3f06b92e, eae8ca02, 33c1a58b, solver code = 505d8399; waiting for pid $WAIT"
[ "$MODE" = dry ] && exit 0
while kill -0 $WAIT 2> /dev/null; do sleep 60; done
say "pid $WAIT has exited"; grep -E '^== .* (lane d18d done|STOP)' $Q/lane_d18d.log
cd $W
for run in "${RUNS[@]}"; do
  set -- $run
  say "D $3: the hybrid at 1.20,2.60 on $(basename $2) (timeout 1800 s)"
  timeout 1800 nice -n 10 $PY -u $Q/d18_hybsign.py $1 $2 $3 1.20,2.60 $OUT < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' >> $LOG
  r=${PIPESTATUS[0]}; say "D $3 exit $r"
  [ $r = 0 ] || { say "STOP: D $3 did not finish (exit $r; 3 = not the record system)"; exit; }
done
cat $LOG
$PY $Q/d18_refsign_read.py $OUT > $RD 2>&1; r=$?
cat $RD; say "reader exit $r"
say "lane d18r done"
exit
}
