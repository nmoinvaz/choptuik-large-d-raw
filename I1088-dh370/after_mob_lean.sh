#!/bin/bash
# after rebuild_mob.sh (the build with the z recurrence, ae0b5453 or later): D 1000 held the lean way, the same guess
# and held values as j1000_held_mob (the 50 chain states, degree 2; --segs_from and --held_from that state), the
# Moebius horizon a 8, the double-double Jacobian and residual stopped by Delta's first-order bound 1e-15, one
# quad-double residual check, the Hamiltonian code check and the discretization report; 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-buildmob; do sleep 30; done
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'set_horizon_mobius')" || exit 1
grep -q "def disc_report" $W/hp/form_s.py || exit 1
R=$W/out/j1000_held_mob/jump_s_D1000.0000.npz
$W/run_jump.sh 1000 252.5 2 0 0 6 lean --held 1 --it_max 10 --kc 200 --delta 1.654240854245 --mob 8 \
  --segs_from $R --held_from $R --tol 1e-300
exit
}
