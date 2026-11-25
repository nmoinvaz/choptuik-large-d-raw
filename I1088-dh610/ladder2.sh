#!/bin/bash
# the held ladder past D 2000 in steps of 1.1 in D (#1088): the guess's horizon mismatch at x_l = 0.7 grows like
# A(n) times the fit's error, A about 10^(0.0087 n) (D 1414 1e3, 2000 2e8, 2828 3e15 from bulk errors 1e-8 .. 1e-10),
# so a sqrt(2) step failed at 2828 (3.2e5). Each rung from the last three converged states at degree 2 in 1/n, the
# Moebius horizon a = max(8, n/400) at 0.7, ks 1.5 n + 20, kc 250, Delta the fit's, the lean defaults without the
# discretization report (--disc 0); stops at the first rung that does not converge; 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
bash $W/update_py.sh > /dev/null
S1=$W/out/j1414_held_mob/jump_s_D1414.0000.npz
S2=$W/out/j2000_held_mob2/jump_s_D2000.0000.npz
S3=$W/out/j2200_l2/jump_s_D2200.0000.npz
for D in 2420 2662 2928 3221 3543 3897 4287 4716 5188; do
  A=$(python3 -c "print(max(8.0, ($D - 2) / 400))")
  export HP_COMMIT=3aecf887
  $W/run_jump.sh $D 225 2 0 0 9 l2 --held 1 --it_max 12 --kc 250 --delta fit --mob $A --states_s "$S1,$S2,$S3" \
    --tol 1e-300 --disc 0 --res od
  grep -q "converged;" $W/out/j${D}_l2/jump.log || exit 1
  grep -q "NOT converged" $W/out/j${D}_l2/jump.log && exit 1
  S1=$S2; S2=$S3; S3=$W/out/j${D}_l2/jump_s_D${D}.0000.npz
done
exit
}
