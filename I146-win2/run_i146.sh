#!/usr/bin/env bash
# #146: #140's six copies plus the rp = 0.081 control, in a loop for 4 h. Each round runs the seven processes in parallel
# into round<k>/, then compare_round.py compares it with round 1, #140 and #104. An anomaly writes ALERT_round<k>.txt and
# the loop goes on. New rounds start until the 4 h mark; the last one may end a few minutes after it.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
W=/c/Users/nathan/Source/choptuik-i140
R=C:/Users/nathan/Source/choptuik-large-d-raw
ROOT=$R/I146-win2
BOX=$R/I104-win2/A_M2_6a_M5_sub1e-18.json
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
T0=$(date +%s); STOP=$(( T0 + 4*3600 ))
echo "driver start $(stamp), new rounds until $(date -u -d @$STOP '+%H:%M:%S') UTC" >> $ROOT/driver.txt
k=1
while [ $(date +%s) -lt $STOP ]; do
  D=$ROOT/round$k; mkdir -p $D; EX=$D/exits.txt
  echo "round $k start $(stamp)" >> $ROOT/driver.txt
  run() {  # run NAME DIR LOG ARGS...
    local name=$1 dir=$2 log=$3; shift 3
    ( cd "$dir" || exit 9; t=$(date +%s)
      "$PY" -u "$@" > "$log" 2>&1; rc=$?
      echo "$name exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $EX ) &
  }
  for i in 1 2 3; do
    run l6a_copy$i $W/solver/proof $D/l6a_copy$i.log lemma6_jump_M.py --M=5 --box=$BOX --rp=0.08 --k=20 \
      --save-B=$D/B_copy$i.json --json=$D/l6a_copy$i.json
  done
  run l6a_control $W/solver/proof $D/l6a_control.log lemma6_jump_M.py --M=5 --box=$BOX --rp=0.081 --k=20 \
    --save-B=$D/B_control.json --json=$D/l6a_control.json
  for i in 1 2 3; do
    run amp_copy$i $W/solver/inner_amp $D/amp_copy$i.log amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys \
      --mf 6:12 --out $D/amp_copy$i.json
  done
  wait
  "$PY" -I $ROOT/compare_round.py $k $ROOT > $D/compare_stdout.txt 2>&1; rc=$?
  echo "round $k end $(stamp), compare exit $rc" >> $ROOT/driver.txt
  if [ $rc -ne 0 ]; then cp $D/compare.txt $ROOT/ALERT_round$k.txt 2>/dev/null || cp $D/compare_stdout.txt $ROOT/ALERT_round$k.txt; fi
  k=$((k+1))
done
echo "driver end $(stamp), rounds run $((k-1))" >> $ROOT/driver.txt
