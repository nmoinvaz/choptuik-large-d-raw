#!/bin/bash
# after rebuild_mob.sh: the D 1000 held jump with the Moebius horizon (a = 8, ks 1.5 n + 20), 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-buildmob; do sleep 30; done
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'set_horizon_mobius')" || exit 1
grep -q "def cmd_mobcheck" $W/hp/form_s.py || exit 1
$W/run_jump.sh 1000 252.5 2 0 0 6 held_mob --held 1 --it_max 10 --kc 200 --delta 1.654240854245 --mob 8
exit
}
