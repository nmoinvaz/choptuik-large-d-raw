#!/bin/bash
# #1098, D 519's machine cross-check, moved from dh170's queue to dh370 (5 threads): the Moebius M 32 tail from mm5's h13
# state (I1098-mm5/ladder/D519/rls/release_ls_h13_D519.0000.npz, blob b5a40765) at mm5's settings (ladder_tail.sh mob,
# sha256 12055ac1..., ks 1196, kmax 23), chord-free (--inner_chord 0), on the Skylake fastmul6 wheel (e1cd7a84, the
# Rust of d368a0c0) with the Python of f398e829. Output into the raw live worktree's I1098-dh370/ladder/D519x (no
# --allow_unraw); push_ladder.sh copies it into the push worktree
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh370/ladder/inputs
mkdir -p $I
cd $LV || exit 1
git cat-file blob b5a407651d6000a594b79000db1d628a975a0732 > $I/D519_rls_h13.npz || exit 2
[ "$(git hash-object --no-filters $I/D519_rls_h13.npz)" = "b5a407651d6000a594b79000db1d628a975a0732" ] || exit 2
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python
export EXTRA="--inner_chord 0" COMMIT=f398e829 KS=1196 KMAX=23
bash $W/out/ladder/ladder_tail.sh mob 519 $I/D519_rls_h13.npz $LV/I1098-dh370/ladder/D519x 5
echo "D 519 check rc $? $(date -u +%H:%M:%S)"
exit
}
