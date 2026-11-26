#!/bin/bash
# #1098, D 2828's M 32 stages on dh170 (coordinator's order, 2026-11-26): waits for unit i1088a-r1549c (D 1549's chord-free
# h13, then its D 519 step, which now ends at once) to end, at most 10 h, then runs ladder_point2.sh (raw blob 8802fb26,
# chord-free, with the k* stage) through rls13 only (STOP_AFTER=rls13): kc 250, KSBAR 1e-70, the tail M 48 and kmax 31
# being for the run on fastmul7 elsewhere. The jump fits in 1/n to D 1549's h13 (this machine's, rls13) and D 2000's
# fastmul6 base h13 (raw I1098-dh610/fix6/D2000_base6, blob b897ba43). The Skylake fastmul6 wheel (e1cd7a84, the Rust of
# d368a0c0), the Python of f398e829, 6 threads. Output into the raw live worktree's I1098-dh170/ladder/D2828 (no
# --allow_unraw)
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh170/ladder/inputs
O=$LV/I1098-dh170/ladder/D2828
n=0
while [ $n -lt 1800 ]; do systemctl --user is-active --quiet i1088a-r1549c || break; sleep 20; n=$((n + 1)); done
systemctl --user is-active --quiet i1088a-r1549c && exit 1
SA0=$W/out/ladder/D1549/rls13/release_ls_h13_D1549.0000.npz
grep -q "^rls h13 rc 0" $W/out/ladder/D1549/run.log && [ -s $SA0 ] || exit 2
mkdir -p $I $O
cp $SA0 $I/D1549_rls13_h13.npz
cd $LV || exit 3
git cat-file blob b897ba43adb46653785b362d2ae6a2f712fdd8db > $I/D2000_base6_h13.npz || exit 3
[ "$(git hash-object --no-filters $I/D2000_base6_h13.npz)" = "b897ba43adb46653785b362d2ae6a2f712fdd8db" ] || exit 3
export HP=$W/hp_y SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
export KSBAR=1e-70 COMMIT=f398e829 STOP_AFTER=rls13 INNER_CHORD=0 EXTRA=
bash $W/out/ladder/tools3/ladder_point2.sh 2828 250 6 $O $I/D1549_rls13_h13.npz $I/D2000_base6_h13.npz 48 31
echo "D 2828 M 32 stages rc $? $(date -u +%H:%M:%S)"
exit
}
