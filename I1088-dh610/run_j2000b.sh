#!/bin/bash
# after the stepping stone D 1414 (unit i1088a-j1414): D 2000 held from the form-S states at D 400, 1000 and 1414 at
# degree 2 in 1/n (no chain states), the Moebius horizon a = max(8, n/400) = 8, ks 1.5 n + 20, kc 250, the lean
# defaults, Delta from Track C's 1.649074313886 +- 1.2e-9 recorded as given; 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-j1414; do sleep 30; done
test -s $W/out/j1414_held_mob/jump_s_D1414.0000.npz || exit 1
grep -q "converged;" $W/out/j1414_held_mob/jump.log || exit 1
bash $W/update_py.sh
S="$W/out/j400_held/jump_s_D400.0000.npz,$W/out/j1000_held_mob/jump_s_D1000.0000.npz,$W/out/j1414_held_mob/jump_s_D1414.0000.npz"
export HP_COMMIT=$(cat $W/hp_commit 2>/dev/null)
$W/run_jump.sh 2000 225 2 0 0 9 held_mob2 --held 1 --it_max 12 --kc 250 --delta 1.649074313886 --mob 8 --states_s "$S" \
  --tol 1e-300 --tc 1.649074313886:1.2e-9
exit
}
