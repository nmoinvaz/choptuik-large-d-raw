#!/bin/bash
# after dh370's fastmul6 build and its checks (all exit 0): ladder points D 622, 747 and 896 by ladder_point2.sh (M 32
# then the tail at M 48, kmax 31), 2 threads each, nice 10, from fastmul6's D 300 and D 1000 states; waits at most 5 h
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 900 ]; do grep -q "^end " $W/build_y.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
grep -q "^end " $W/build_y.log || exit 1
[ "$(grep -c "exit=0" $W/out/fastmul6_build/exit_codes.txt)" = "6" ] || exit 2
export HP=$W/hp_y SITE=$W/site_y PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python EXTRA=--allow_unraw
cp $W/resample_m.py $W/ladder_point2.sh $W/out/ladder/ 2>/dev/null
I=$W/out/ladder/inputs
for d in 622 747 896; do
  mkdir -p $W/out/ladder/D$d
  bash $W/out/ladder/ladder_point2.sh $d 200 2 $W/out/ladder/D$d $I/S300.npz $I/S1000.npz 48 31 &
done
wait
exit
}
