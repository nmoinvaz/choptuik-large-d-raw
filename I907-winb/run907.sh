#!/bin/bash
# #907 on winb, for Git Bash: the two m03up walks of #897 continued from their ends with up to 800 Jacobians, two at a
# time, then one Jacobian from the D 10.5 end. Only the four path lines below may be changed to match the machine.
WT=/c/Users/nathan/Source/choptuik-i897
PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
R=$RAW/I907-winb
export PYTHONUTF8=1 OPENBLAS_NUM_THREADS=3
cd $WT/solver/matter || exit 9
grep -q 'settle' sigdss_band.py || { echo "STOP: sigdss_band.py has no --settle"; exit 9; }
mkdir -p $R
log() { echo "907 $1 $(date -u '+%F %T') UTC" >> $R/exits_907.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import numpy, scipy, sys, platform; print('numpy', numpy.__version__, 'scipy', scipy.__version__, platform.platform(), platform.machine(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # name, then the command's arguments
  local name=$1; shift
  log "$name start"
  local t=$(date +%s)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t )) s"
}
E=3.33333333333
I=$RAW/I897-winb
for f in walk2_up_10.0 walk2_up_10.5; do
  [ -f $I/$f.npy ] || { log "STOP: no $I/$f.npy"; exit 9; }
done
W="--eps $E --kc 15 --maxjac 800 --settle 3"
run walk3_up_10.0 sigdss_band.py walk $I/walk2_up_10.0.npy --D 10   $W --out $R/walk3_up_10.0.npy --json $R/walk3_up_10.0.jsonl &
run walk3_up_10.5 sigdss_band.py walk $I/walk2_up_10.5.npy --D 10.5 $W --out $R/walk3_up_10.5.npy --json $R/walk3_up_10.5.jsonl &
wait
run jac1_up_10.5 sigdss_band.py walk $I/walk2_up_10.5.npy --D 10.5 --eps $E --kc 15 --maxjac 1 --settle 3 --out $R/jac1_up_10.5.npy --json $R/jac1_up_10.5.jsonl
for w in up_10.0:10 up_10.5:10.5; do
  n=${w%%:*}; d=${w##*:}
  [ -f $R/walk3_$n.npy ] && run width3_$n sigdss_band.py width $R/walk3_$n.npy --D $d --eps $E --kc 15 --json $R/width3.jsonl
done
log "done"
