#!/bin/bash
# #892 on rpi5 (the coordinator): sigdss at eta = 0.3, the march's states at D 8 to 11 in the system without the
# smoothness prior. sigdss_band.py width at each state, walks without the prior from the five prior-carrying states (two
# at a time), width at each walk's end, and the D 8.0 control walk. Every output goes to the raw folder.
R=/home/nathan/Source/choptuik-large-d-raw/I892-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-892
cd $WT/solver/matter || exit 9
mkdir -p $R
log() { echo "892 $1 $(date -u '+%F %T') UTC" >> $R/exits_892.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import numpy, scipy, sys, platform; print('numpy', numpy.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
export OPENBLAS_NUM_THREADS=2
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  nice -n 10 $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
E=3.33333333333
B=sigdss_band.py
# 1. widths at the march's states (D 8.0 has no prior: the control)
run run width_up_8.0   $B width data/sigdss_m03up.npz@8.0  --D 8    --eps $E --kc 15 --json $R/width.jsonl
run run width_up_9.0   $B width data/sigdss_m03up.npz@9.0  --D 9    --eps $E --kc 15 --json $R/width.jsonl
run run width_up_10.0  $B width data/sigdss_m03up.npz@10.0 --D 10   --eps $E --kc 15 --json $R/width.jsonl
run run width_up_10.5  $B width data/sigdss_m03up.npz@10.5 --D 10.5 --eps $E --kc 15 --json $R/width.jsonl
run run width_hi_10.5  $B width data/sigdss_m03hi.npz@10.5 --D 10.5 --eps $E --kc 15 --json $R/width.jsonl
run run width_hi_11.0  $B width data/sigdss_m03hi.npz@11.0 --D 11   --eps $E --kc 15 --json $R/width.jsonl
# 4. the control first: a short walk from D 8.0 must stay within its width
run ctrl walk_up_8.0   $B walk data/sigdss_m03up.npz@8.0 --D 8 --eps $E --kc 15 --maxjac 20 --out $R/walk_up_8.0.npy --json $R/walk.jsonl
# 2. walks without the prior, two at a time
run run walk_up_9.0    $B walk data/sigdss_m03up.npz@9.0  --D 9    --eps $E --kc 15 --maxjac 150 --out $R/walk_up_9.0.npy  --json $R/walk_up_9.0.jsonl &
run run walk_up_10.0   $B walk data/sigdss_m03up.npz@10.0 --D 10   --eps $E --kc 15 --maxjac 150 --out $R/walk_up_10.0.npy --json $R/walk_up_10.0.jsonl &
wait
run run walk_up_10.5   $B walk data/sigdss_m03up.npz@10.5 --D 10.5 --eps $E --kc 15 --maxjac 150 --out $R/walk_up_10.5.npy --json $R/walk_up_10.5.jsonl &
run run walk_hi_10.5   $B walk data/sigdss_m03hi.npz@10.5 --D 10.5 --eps $E --kc 15 --maxjac 150 --out $R/walk_hi_10.5.npy --json $R/walk_hi_10.5.jsonl &
wait
run run walk_hi_11.0   $B walk data/sigdss_m03hi.npz@11.0 --D 11   --eps $E --kc 15 --maxjac 150 --out $R/walk_hi_11.0.npy --json $R/walk_hi_11.0.jsonl
# 3. widths at the walks' ends
for w in up_8.0:8 up_9.0:9 up_10.0:10 up_10.5:10.5 hi_10.5:10.5 hi_11.0:11; do
  n=${w%%:*}; d=${w##*:}
  [ -f $R/walk_$n.npy ] && run run width_end_$n $B width $R/walk_$n.npy --D $d --eps $E --kc 15 --json $R/width_end.jsonl
done
log "all done"
