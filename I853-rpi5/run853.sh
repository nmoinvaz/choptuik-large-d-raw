#!/bin/bash
# #853 on rpi5 (the coordinator): lemma 6b1(5), the covering behind Theorem A(M = 5), reproduced on aarch64 Linux with
# #121's commands (I121-win2/run_i121.sh): the C1 ray run first (every row continues from its final state), then the 18
# rows in four processes, then the covering check and its two controls. Tag _rpi5, so every row is computed here.
R=/home/nathan/Source/choptuik-large-d-raw/I853-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-853
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "853 $1 $(date -u '+%F %T') UTC" >> $R/exits_853.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
X=2.71857918921174241298383648012843280883,0.99922840320656778341382852244561290493,0.14920357491144750568385993252030607895,0.01471905249025135288037099322184756733,0.00840534690576166107173716067740959800,0.00147034518159157802673581431742815600
C="--M=5 --x=$X --h=1e-18 --tag=_rpi5"
run run ray lemma6b1_cover_M.py ray --c1 $C
[ -f lemma6b1_runs_M5_rpi5/ray.json ] || { log "STOP: no ray.json"; exit 9; }
# four groups, balanced on #121's process times (rows 5-9 the slowest)
run run rows_1 lemma6b1_cover_M.py rows $C --only=5,6,7,8,9 &
run run rows_2 lemma6b1_cover_M.py rows $C --only=0,1,12,16 &
run run rows_3 lemma6b1_cover_M.py rows $C --only=2,10,11,13,17 &
run run rows_4 lemma6b1_cover_M.py rows $C --only=3,4,14,15 &
wait
run run  check        lemma6b1_cover_M.py check $C --json=$R/lemma6b1_check_M5_rpi5.json
run ctrl check_drop   lemma6b1_cover_M.py check $C --drop=9,5
run ctrl mutate_row00 lemma6b1_cover_M.py mutate --M=5 --j=0 --x=$X --h=1e-18 --tag=_rpi5
cp -r lemma6b1_runs_M5_rpi5 $R/
log "all done"
