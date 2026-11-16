#!/bin/bash
# #897 on winb (the coordinator), for Git Bash: sigdss at eta = 0.3 without the smoothness prior, the walks of #892
# continued from their end states (raw I892-rpi5/walk_*.npy) with --settle 3 and up to 400 Jacobians, two at a time,
# then width at each end. Only the four path lines below may be changed to match the machine; nothing else.
WT=/c/Users/nathan/Source/choptuik-i897
PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
R=$RAW/I897-winb
export PYTHONUTF8=1 OPENBLAS_NUM_THREADS=3
cd $WT/solver/matter || exit 9
grep -q 'settle' sigdss_band.py || { echo "STOP: sigdss_band.py has no --settle (main 361615da or later is needed)"; exit 9; }
mkdir -p $R
log() { echo "897 $1 $(date -u '+%F %T') UTC" >> $R/exits_897.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import numpy, scipy, sys, platform; print('numpy', numpy.__version__, 'scipy', scipy.__version__, platform.platform(), platform.machine(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind, name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t )) s ($kind)"
}
E=3.33333333333
I=$RAW/I892-rpi5
for f in walk_up_10.0 walk_up_10.5 walk_hi_10.5 walk_hi_11.0; do
  [ -f $I/$f.npy ] || { log "STOP: no $I/$f.npy (pull the raw worktree)"; exit 9; }
done
W="--eps $E --kc 15 --maxjac 400 --settle 3"
run run walk2_up_10.0 sigdss_band.py walk $I/walk_up_10.0.npy --D 10   $W --out $R/walk2_up_10.0.npy --json $R/walk2_up_10.0.jsonl &
run run walk2_up_10.5 sigdss_band.py walk $I/walk_up_10.5.npy --D 10.5 $W --out $R/walk2_up_10.5.npy --json $R/walk2_up_10.5.jsonl &
wait
run run walk2_hi_10.5 sigdss_band.py walk $I/walk_hi_10.5.npy --D 10.5 $W --out $R/walk2_hi_10.5.npy --json $R/walk2_hi_10.5.jsonl &
run run walk2_hi_11.0 sigdss_band.py walk $I/walk_hi_11.0.npy --D 11   $W --out $R/walk2_hi_11.0.npy --json $R/walk2_hi_11.0.jsonl &
wait
for w in up_10.0:10 up_10.5:10.5 hi_10.5:10.5 hi_11.0:11; do
  n=${w%%:*}; d=${w##*:}
  [ -f $R/walk2_$n.npy ] && run run width2_$n sigdss_band.py width $R/walk2_$n.npy --D $d --eps $E --kc 15 --json $R/width2.jsonl
done
log "all done"
