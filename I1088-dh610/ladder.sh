#!/bin/bash
# the held ladder in steps of about sqrt(2) in n (#1088): after D 2000 (unit i1088a-j2000b), D 2828, 4000, 5657, 8000
# and 10000, each from the last three converged form-S states at degree 2 in 1/n (a jump reaches about sqrt(2) in n:
# I1088-mac-a/form_s/gain_f64.log), the Moebius horizon a = max(8, n/400), ks 1.5 n + 20, kc 250, Delta the fit's, the
# lean defaults; stops at the first rung that does not converge; 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-j2000b; do sleep 60; done
S1=$W/out/j1000_held_mob/jump_s_D1000.0000.npz
S2=$W/out/j1414_held_mob/jump_s_D1414.0000.npz
S3=$W/out/j2000_held_mob2/jump_s_D2000.0000.npz
grep -q "converged;" $W/out/j2000_held_mob2/jump.log || exit 1
for D in 2828 4000 5657 8000 10000; do
  bash $W/update_py.sh > /dev/null
  A=$(python3 -c "print(max(8.0, ($D - 2) / 400))")
  export HP_COMMIT=$(cat $W/hp_commit 2>/dev/null)
  $W/run_jump.sh $D 225 2 0 0 9 ladder --held 1 --it_max 12 --kc 250 --delta fit --mob $A --states_s "$S1,$S2,$S3" \
    --tol 1e-300
  grep -q "converged;" $W/out/j${D}_ladder/jump.log || exit 1
  S1=$S2; S2=$S3; S3=$W/out/j${D}_ladder/jump_s_D${D}.0000.npz
done
exit
}
