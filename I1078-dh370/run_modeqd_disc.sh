#!/bin/bash
# #1078, t5's order (hc 2026-11-24): the discriminator for the quad-double pair: qd determinants at lambda 5.1408197887857 and 5.1408197887866 (mode_qd.py main 61b8498f, blob 1878985c; same state, plan, kernel, threads as the pair),
# run after the update_dd control pair (unit i1078z) ends; checked by disc_check.py against the line through the zero that the pair implies (reading (a)); pass: sign as predicted and |ln - predicted| <= 0.1 at both. Unit i1078d, 4 threads, nice 10.
# Log: steps_modeqd_disc.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WTQ=/home/nathan/Source/choptuik-large-d-1078q
WTM=/home/nathan/Source/choptuik-large-d-1078m
PY=$WTM/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_modeqd_disc.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
step "waiting for unit i1078z (the update_dd control pair) to end"
while [ "$(systemctl --user is-active i1078z)" = active ]; do sleep 20; done
cd $WTQ/hp || exit 9
[ "$(git -C $WTQ rev-parse --short=8 HEAD)" = 61b8498f ] && [ "$(blob mode_qd.py)" = 1878985c ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ -s $OUT/modeqd_pair.jsonl ] || { step "STOP: worktree, mode_qd.py, the state or the pair rows not as pinned"; echo "DISC NOT RUN $(stamp) UTC" > $OUT/MODEQD_DISC_DONE.txt; exit 1; }
python3 $OUT/disc_check.py selftest > $OUT/disc_check_selftest.txt 2>&1 && ! python3 $OUT/disc_check.py selftest --mutate=x > /dev/null 2>&1 || true
t0=$(date +%s)
nice -n 10 $PY -u mode_qd.py $OUT/modeqd_disc.jsonl $S96 5.1408197887857 5.1408197887866 --threads=4 > $OUT/modeqd_disc.log 2>&1; rc=$?
step "qd at 5.1408197887857 and 5.1408197887866: exit $rc, $(( $(date +%s) - t0 )) s; $(grep -v Warning $OUT/modeqd_disc.log | cut -c1-250 | tr '\n' '|')"
python3 $OUT/disc_check.py $OUT/modeqd_pair.jsonl $OUT/modeqd_disc.jsonl --bar=0.1 > $OUT/modeqd_disc_check.txt 2>&1; rcc=$?
step "disc_check: exit $rcc (0 = on the line); $(cut -c1-400 $OUT/modeqd_disc_check.txt | tr '\n' '|')"
echo "MODEQD DISC DONE: qd exit $rc, check exit $rcc $(stamp) UTC" > $OUT/MODEQD_DISC_DONE.txt
exit 0
}
