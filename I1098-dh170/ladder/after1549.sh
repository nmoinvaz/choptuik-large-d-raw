#!/bin/bash
# after D 1549's M 32 stages (unit i1088a-ladder1549b, STOP_AFTER=rls13), at most 12 h: D 519's machine cross-check, the
# Moebius M 32 tail from mm5's h13 state (I1098-mm5/ladder/D519/rls/release_ls_h13_D519.0000.npz) at mm5's settings
# (ladder_tail.sh mob, ks 1196, kmax 23), 6 threads, on the Skylake fastmul6 wheel with Python f398e829 (inner chord on;
# mm5's ran 478e9d86 with it off): the same kernel source (d368a0c0) and the same input, another machine and Python
{
W=/home/nathan/Source/choptuik-large-d-1088a
n=0
while [ $n -lt 2160 ]; do systemctl --user is-active --quiet i1088a-ladder1549b || break; sleep 20; n=$((n + 1)); done
systemctl --user is-active --quiet i1088a-ladder1549b && exit 1
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python EXTRA=--allow_unraw
export COMMIT=f398e829 KS=1196 KMAX=23
bash $W/out/ladder/ladder_tail.sh mob 519 $W/out/ladder/inputs/D519_rls_h13.npz $W/out/ladder/D519x/tail_mob 6
exit
}
