#!/bin/bash
# the stepping stone D 1414 (#1088): the D 2000 guess from D <= 1000 is outside the basin (horizon mismatch 1.7-20,
# gain from m_h 1.4e5 at the guess), while the same fit at D 1414 reads 1.6e-5 (I1088-mac-a/form_s/gain_f64.log).
# Held, the Moebius horizon a = max(8, n/400) = 8, ks 1.5 n + 20, kc 220, the guess from the form-S states at D 300
# (released), 400 (held) and 1000 (held) at degree 2 in 1/n (no chain states), Delta the fit's; the lean defaults
# (double-double solve to Delta's bound 1e-15, one quad-double check, the discretization report, the Hamiltonian check);
# 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
S="$W/out/rls300/release_ls_h13_D300.0000.npz,$W/out/j400_held/jump_s_D400.0000.npz,$W/out/j1000_held_mob/jump_s_D1000.0000.npz"
export HP_COMMIT=bf90d450
$W/run_jump.sh 1414 225 2 0 0 9 held_mob --held 1 --it_max 12 --kc 220 --delta fit --mob 8 --states_s "$S" --tol 1e-300
exit
}
