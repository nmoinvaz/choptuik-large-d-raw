#!/bin/bash
# #1098 on dh610 (coordinator, 2026-11-28), after its move: D 6666's tail resumed from the same state as mm5's part B
# (d4628k_d6666r_mm5.sh, raw 68735e257), dh610's own h15 step state release_ls_h15_D6666.0000_step.npz (blob a89b9788),
# on dh610's fastmul7 (hp_z, site_z, Python c21ba40d), 12 threads, into D6666/tail_x, then its k* stage. mm5's run and
# this one start from one state on two machines and two Python commits of fastmul7: their final Delta differences are
# the ladder's machine cross-check at D 6666 (err_xcheck_machine).
# release_ls with ladder_tail.sh's options (--harm 15,...,23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25, outer 8,
# chord-free) under timeout 16h, then kmax_rule.py and kstar_stage.sh (its own 3 h limit on the re-converge).
# "job rc N" ends run.log.
#
#     d6666x_610.sh      (detached: systemd-run --user)
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
L=$LV/I1098-dh610/ladder
T=$L/tools3
S=$L/D6666/tail/release_ls_h15_D6666.0000_step.npz
O=$L/D6666/tail_x
export HP=$W/hp_z SITE=$W/site_z PY=$(cat $W/python_path) COMMIT=c21ba40d
for f in kmax_rule.py:196f12a553edce9651fef58ef90353f3c7fb49b4 kstar_stage.sh:6d29dfc0225a2eff0be932cb849e656c190a0b6e; do
  [ "$(git -C $LV hash-object --no-filters $T/${f%%:*})" = "${f#*:}" ] || { echo "tools3/${f%%:*}: blob differs"; exit 1; }
done
[ "$(git -C $LV hash-object --no-filters $S)" = a89b97885355fffd9dc103412e2493324d029655 ] || { echo "start state: blob differs"; exit 1; }
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC, D 6666 tail from dh610's h15 step state (cross-check of mm5's part B), commit $COMMIT" > $O/run.log
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
cd $HP || exit 1
PYTHONPATH=$SITE nice -n 10 timeout 16h $PY -u form_s.py release_ls $S $O --harm 15,17,19,21,23 --kmax 23 \
  --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 12 --outer 8 \
  --inner_chord 0 --commit $COMMIT > $O/rls.log 2>&1
r=$?
echo "rls h15-h23 rc $r $(date -u +%H:%M:%S)" >> $O/run.log
[ -s $O/release_ls_h23_D6666.0000.npz ] || { echo "job rc 3 $(date -u +%H:%M:%S)" >> $O/run.log; exit 3; }
$PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
echo "kmax_rule rc $? ($(tail -1 $O/kmax_rule.log))" >> $O/run.log
HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar 12
r=$?
echo "kstar rc $r $(date -u +%H:%M:%S)" >> $O/run.log
echo "job rc $r $(date -u +%H:%M:%S)" >> $O/run.log
exit $r
}
