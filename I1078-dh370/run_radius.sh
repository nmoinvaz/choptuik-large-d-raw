#!/bin/bash
# #1078, t5's order (comment of 22:20 UTC, run 1; unit i1078t): highm_diag.py radius on the D 3.044375 M' 96 state (6a0f83d2) and the D 3.15 M' 96 L0.7 state (9e683a14), as given
# (highm_diag's own, unmapped solver) and with the state's own mapped solver (radius_mapped.py); the control: the uniform D 3.15 M 128 state (df2ab378, no map), where the two must be equal.
# Worktree ~/Source/choptuik-large-d-1078 at main 3279c81f, the c016b932 kernel of its venv, 2 threads, nice 10. Log: steps_radius.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
S315=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
S128U=$RAWIN/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_radius.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 3279c81f ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $S315)" = 9e683a14 ] && [ "$(blob $S128U)" = df2ab378 ] || { step "STOP: worktree or a state not pinned"; echo "RADIUS NOT RUN $(stamp) UTC" > $OUT/RADIUS_DONE.txt; exit 1; }
step "start; highm_diag.py blob $(blob highm_diag.py); load $(cut -d' ' -f1-3 /proc/loadavg)"
for tag in D3.0444_M96:$S96:96 D3.15_M96:$S315:96 D3.15_M128_uniform:$S128U:128; do
  name=${tag%%:*}; rest=${tag#*:}; f=${rest%%:*}; M=${rest##*:}
  t0=$(date +%s)
  nice -n 10 $PY highm_diag.py radius $f $M > $OUT/radius_${name}_as_given.txt 2>&1; r1=$?
  nice -n 10 $PY $OUT/radius_mapped.py $f $M > $OUT/radius_${name}_mapped.txt 2>&1; r2=$?
  nice -n 10 $PY $OUT/radius_mapped.py $f $M --as_given > $OUT/radius_${name}_ctl.txt 2>&1; r3=$?
  if diff -q <(grep -v RuntimeWarning $OUT/radius_${name}_as_given.txt) <(grep -v RuntimeWarning $OUT/radius_${name}_ctl.txt) > /dev/null; then c=same; else c=DIFFERENT; fi
  if diff -q <(grep -v RuntimeWarning $OUT/radius_${name}_as_given.txt) <(grep -v RuntimeWarning $OUT/radius_${name}_mapped.txt) > /dev/null; then m=same; else m=different; fi
  step "$name: highm_diag radius exit $r1, mapped variant exit $r2, as-given through the wrapper exit $r3 ($c as highm_diag.py's own), mapped against as given: $m; $(( $(date +%s) - t0 )) s"
done
echo "RADIUS DONE $(stamp) UTC" > $OUT/RADIUS_DONE.txt
exit 0
}
