#!/bin/bash
# D 896 (unit i1088a-ladder896b, Python f398e829 with inner chord steps on): kept through its h5-h11 release, then
# stopped, and h13 and the M 48 tail (kmax 23) run chord-free (--inner_chord 0), the path D 432-622 took. mm5's D 747
# on f398e829 stopped at h13 outer 1, its qq inner solve at 1.75e-45 after 10 steps against tol 1e-48
{
W=/home/nathan/Source/choptuik-large-d-1088a
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python
export EXTRA="--allow_unraw --inner_chord 0" COMMIT=f398e829 UNIT=i1088a-ladder896b WAIT_H=4
bash $W/out/ladder/ladder_from_h11.sh 896 6 $W/out/ladder/D896 48 23
exit
}
