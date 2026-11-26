#!/bin/bash
# waits for wave 2's D1000_base (at most 2 h), then the d/dtheta pair (dmat.sh) from its re-converged state
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/fix/D1000_base
n=0
while [ $n -lt 360 ]; do grep -q "^end " $O/run.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
grep -q "^rc 0" $O/run.log || exit 1
[ -s $O/release_ls_h13_D1000.0000.npz ] || exit 2
$W/dmat.sh D1000 $O/release_ls_h13_D1000.0000.npz
exit
}
