#!/usr/bin/env bash
# #204: the amplitude copy on Python 3.14 in a loop, on the cores #202 and #196 leave free. Each round runs N copies (N is
# the number in the file COPIES, 3 if absent, read at each round start) of
# `amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12` in parallel into round<k>/, then compare_amp.py compares
# the JSONs with #161's hash. An anomaly copies compare.txt to ALERT_round<k>.txt and the loop goes on. It stops after the
# round during which the file STOP appears. Normal priority, no affinity, one thread per copy. As #177's run_i177.sh, with
# the checkout and raw repository on D: (the project moved) and main's solver/inner_amp instead of the I140 worktree.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
W=/d/choptuik-large-d
ROOT=D:/choptuik-large-d-raw/I204-win2
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
echo "driver start $(stamp)" >> $ROOT/driver.txt
k=$(( $(ls -d $ROOT/round* 2>/dev/null | wc -l) + 1 ))
while [ ! -e $ROOT/STOP ]; do
  n=3; [ -f $ROOT/COPIES ] && n=$(cat $ROOT/COPIES)
  D=$ROOT/round$k; mkdir -p $D; EX=$D/exits.txt
  echo "round $k start $(stamp), $n copies" >> $ROOT/driver.txt
  for i in $(seq 1 $n); do
    ( cd $W/solver/inner_amp || exit 9; t=$(date +%s)
      "$PY" -u amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12 --out $D/amp_copy$i.json > $D/amp_copy$i.log 2>&1; rc=$?
      echo "amp_copy$i exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $EX ) &
  done
  wait
  "$PY" -I $ROOT/compare_amp.py $k $ROOT > $D/compare_stdout.txt 2>&1; rc=$?
  echo "round $k end $(stamp), compare exit $rc" >> $ROOT/driver.txt
  if [ $rc -ne 0 ]; then cp $D/compare.txt $ROOT/ALERT_round$k.txt 2>/dev/null || cp $D/compare_stdout.txt $ROOT/ALERT_round$k.txt; fi
  k=$((k+1))
done
echo "driver end $(stamp), rounds run $((k-1))" >> $ROOT/driver.txt
