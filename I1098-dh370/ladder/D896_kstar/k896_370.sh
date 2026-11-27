#!/bin/bash
# #1098 D 896's k* stage (Track A, 2026-11-27): kstar_stage.sh (tools3, blob 6d29dfc0) on the M 48 tail of
# out/ladder/D896/tail (i1088a-r896c, ended rc 0 at 00:39:40), into the live raw worktree's I1098-dh370/ladder/D896_kstar:
# the gain at kfreeze 15 at the tail's final state (h23), and when gain x F(15) > 1e-27 the k* system re-converged from
# the h15 state (release_ls --harm 15 --kmax 15, qq, od, tol 1e-62), chord-free; the tail's kernel and Python (Skylake
# wheel site_sky, hp_y at f398e829), 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
T=$LV/I1098-dh370/ladder/tools3
O=$LV/I1098-dh370/ladder/D896_kstar
[ "$(git -C $LV hash-object --no-filters $T/kstar_stage.sh)" = "6d29dfc0225a2eff0be932cb849e656c190a0b6e" ] || exit 2
mkdir -p $O
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python COMMIT=f398e829
export INNER_CHORD=0 EXTRA=
bash $T/kstar_stage.sh $W/out/ladder/D896/tail $O 6
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
