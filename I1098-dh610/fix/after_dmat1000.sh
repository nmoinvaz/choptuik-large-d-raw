#!/bin/bash
# waits for the D 1000 d/dtheta pair (at most 2 h), then the D 2000 pair (dmat.sh) from rls2000d's full M 32 state
# (Moebius a 8, ks 2618, kfreeze 13); the term is (Delta_16 - Delta_12) / (2^16 - 2^12), which needs no base run
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 360 ]; do
  c=$(grep -h "^end " $W/out/fix/D1000_dmat16/run.log $W/out/fix/D1000_dmat12/run.log 2>/dev/null | wc -l)
  [ "$c" -ge 2 ] && break
  sleep 20; n=$((n + 1))
done
S=$W/out/rls2000d/release_ls_h13_D2000.0000.npz
[ -s $S ] || exit 2
$W/dmat.sh D2000 $S
exit
}
