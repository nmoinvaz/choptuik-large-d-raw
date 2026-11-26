#!/bin/bash
# waits for install_sky.sh's D 1549 run (unit i1088a-sky, the ladder_point2.sh with the ks-gate parse bug, which ends
# with exit 6 after its jump) to end, at most 3 h, then restarts D 1549 with the fixed ladder_point2.sh (651bb75f), which
# keeps the converged jump, through rls13 only (STOP_AFTER=rls13): the M 48 tail runs on mm5 from the h13 state
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 540 ]; do systemctl --user is-active --quiet i1088a-sky || break; sleep 20; n=$((n + 1)); done
systemctl --user is-active --quiet i1088a-sky && exit 1
grep -q "STOP_AFTER" $W/out/ladder/ladder_point2.sh || exit 2
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python EXTRA=--allow_unraw
export KSBAR=1e-70 COMMIT=f398e829 STOP_AFTER=rls13
I=$W/out/ladder/inputs
echo "restart $(date -u +%H:%M:%S)" >> $W/out/ladder/D1549/run.log
bash $W/out/ladder/ladder_point2.sh 1549 230 6 $W/out/ladder/D1549 $I/S300.npz $I/S1000.npz 48 31
exit
}
