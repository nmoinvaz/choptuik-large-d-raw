#!/bin/bash
# #1072 step 0: environment and checks (unit i1072a). Writes step0.txt and STEP0_VERDICT.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
WT=/home/nathan/Source/choptuik-large-d-1072
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $WT/hp || exit 9
stamp() { date -u '+%F %T'; }
echo "$(stamp) UTC step 0 starts; worktree $(git -C $WT rev-parse --short=8 HEAD); load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/step0.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 46a8dac5 ] || { echo "REFUSED: worktree not at 46a8dac5" > $OUT/STEP0_VERDICT.txt; exit 1; }
nice -n 10 $PY tau_map_gain.py selftest > $OUT/selftest_tau_map_gain.txt 2>&1; a=$?
echo "$(stamp) UTC tau_map_gain.py selftest exit $a (0 wanted)" >> $OUT/step0.txt
nice -n 10 $PY tau_map_gain.py selftest --mutate gp > $OUT/selftest_tau_map_gain_mutate_gp.txt 2>&1; b=$?
echo "$(stamp) UTC tau_map_gain.py selftest --mutate gp exit $b (1 wanted)" >> $OUT/step0.txt
nice -n 10 $PY lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6 > $OUT/selftest_lowD_gamma.txt 2>&1; c=$?
echo "$(stamp) UTC lowD_gamma.py --selftest (M96 D 3.7 state) exit $c (0 wanted)" >> $OUT/step0.txt
nice -n 10 $PY lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6 --break > $OUT/selftest_lowD_gamma_break.txt 2>&1; d=$?
echo "$(stamp) UTC lowD_gamma.py --selftest --break exit $d (1 wanted)" >> $OUT/step0.txt
nice -n 10 $PY -c "
import sys; sys.path.insert(0, '.')
import tau_map
s = tau_map.make_solver_mapped(3.15, 24, 0.5, 0.4, threads=2)
print('make_solver_mapped(3.15, 24, 0.5, 0.4) constructed', type(s).__name__)" > $OUT/make_solver_mapped.txt 2>&1; e=$?
echo "$(stamp) UTC make_solver_mapped constructs a solver: exit $e (0 wanted); $(tail -1 $OUT/make_solver_mapped.txt | cut -c1-150)" >> $OUT/step0.txt
if [ $a = 0 ] && [ $b = 1 ] && [ $c = 0 ] && [ $d = 1 ] && [ $e = 0 ]; then echo "STEP 0 PASS $(stamp) UTC" > $OUT/STEP0_VERDICT.txt; else echo "STEP 0 FAIL exits $a $b $c $d $e (0 1 0 1 0 wanted)" > $OUT/STEP0_VERDICT.txt; fi
echo "$(stamp) UTC $(cat $OUT/STEP0_VERDICT.txt)" >> $OUT/step0.txt
exit 0
}
