#!/bin/bash
# D 1549 (unit i1088a-ladder1549b, Python f398e829 with inner chord steps on): kept through its h5-h11 release, then
# stopped, and h13 run chord-free (--inner_chord 0) at M 32, ending there (STOP_AFTER=rls13; the M 48 tail runs on mm5).
# mm5's D 747 on f398e829 stopped at h13 outer 1, its qq inner solve at 1.75e-45 after 10 steps against tol 1e-48.
# Then D 519's machine cross-check, as after1549.sh (unit i1088a-d519x, stopped) but chord-free: the Moebius M 32 tail
# from mm5's h13 state (I1098-mm5/ladder/D519/rls/release_ls_h13_D519.0000.npz) at mm5's settings (ks 1196, kmax 23)
{
W=/home/nathan/Source/choptuik-large-d-1088a
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
export EXTRA="--allow_unraw --inner_chord 0" COMMIT=f398e829
UNIT=i1088a-ladder1549b STOP_AFTER=rls13 WAIT_H=8 bash $W/out/ladder/ladder_from_h11.sh 1549 6 $W/out/ladder/D1549 48 31
echo "D 1549 resume rc $? $(date -u +%H:%M:%S)"
KS=1196 KMAX=23 bash $W/out/ladder/ladder_tail.sh mob 519 $W/out/ladder/inputs/D519_rls_h13.npz $W/out/ladder/D519x/tail_mob 6
echo "D 519 check rc $? $(date -u +%H:%M:%S)"
exit
}
