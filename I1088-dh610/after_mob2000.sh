#!/bin/bash
# after rebuild_mob.sh (build, mobcheck at D 400): the D 2000 held jump with the Moebius horizon, a = max(8, n/400) = 8,
# ks 1.5 n + 20, kc 250, the quad-double Jacobian, Delta from Track C's 1.649074313886; the guess from the 50 chain states
# and the form-S states at D 250 (held), 300 (released) and 400 (held), degree 2 in 1/n; 9 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-buildmob; do sleep 30; done
bash $W/update_py.sh
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'set_horizon_mobius')" || exit 1
S="$W/out/j250_held/jump_s_D250.0000.npz,$W/out/rls300/release_ls_h13_D300.0000.npz,$W/out/j400_held/jump_s_D400.0000.npz"
$W/run_jump.sh 2000 252.5 2 0 0 9 held_mob --held 1 --it_max 12 --kc 250 --delta 1.649074313886 --mob 8 --states_s "$S"
exit
}
