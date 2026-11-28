#!/bin/bash
# #1098 on mm5 (coordinator, 2026-11-28): the two ladder runs that dh610 left when it was stopped for a move
# (raw 37e499d20, I1098-dh610/ladder/), on mm5's fastmul7 (choptuik-fastmul7, fastmul7-site, venv-314):
#   A. D 4628's k* stage (kstar_stage.sh, tools3 blob 6d29dfc0), 4 threads: dh610 finished the tail to h23 and the gain
#      (1.186286e33, bound 8.8e-19, so a re-converge), and was stopped one hour into the re-converge. Here it runs again
#      on a copy of the tail's release_ls.jsonl, h15 and h23 states, into D4628m/tail/kstar.
#   B. D 6666's tail resumed, 10 threads: dh610 released h13 and took h15's outer step 0, saved as
#      release_ls_h15_D6666.0000_step.npz (h15 outer 1 was not finished). release_ls from that state with
#      ladder_tail.sh's options (--harm 15,...,23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25, outer 8, chord-free)
#      into D6666m/tail, then the k* stage there. The record joins dh610's release_ls.jsonl (h13, h15 outer 0) and this
#      one's.
# PYTHONPATH=$SITE on B's release_ls was missing in blob 20038ad9 (mm5 set it in the environment of the run that
# started 03:39:12 UTC, so that run is on fastmul7-site). A and B run at once. Each input is copied from raw origin and its blob checked first. Stop rules: release_ls under
# timeout 16h (B), the k* stage's own 3 h limit on its re-converge; "job rc N" ends each part's run.log.
#
#     d4628k_d6666r_mm5.sh A|B      (detached, one process per part)
{
P=$1
R=$HOME/Source/choptuik-large-d-raw
L=$R/I1098-mm5/ladder
T=$L/tools3
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python
COMMIT=$(git -C $HP rev-parse --short=8 HEAD)
[ "$(git -C $R hash-object --no-filters $T/kstar_stage.sh)" = 6d29dfc0225a2eff0be932cb849e656c190a0b6e ] || { echo "kstar_stage.sh blob differs"; exit 1; }
git -C $R fetch -q origin || exit 1
get() {  # raw path, blob, destination
  git -C $R show origin/main:$1 > $3 && [ "$(git -C $R hash-object --no-filters $3)" = "$2" ] || { echo "input $1: blob differs"; exit 1; }
}
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1
S=I1098-dh610/ladder
if [ "$P" = A ]; then
  O=$L/D4628m/tail
  mkdir -p $O
  get $S/D4628_x706/tail/release_ls.jsonl f4bff4b6cc07c0dbede34975814131fd425c3989 $O/release_ls.jsonl
  get $S/D4628_x706/tail/release_ls_h15_D4628.0000.npz c64ef01269c779d465e5a621829f9a41121009cd $O/release_ls_h15_D4628.0000.npz
  get $S/D4628_x706/tail/release_ls_h23_D4628.0000.npz 717aea659cf86342e977fd1f04ab4bedb6f77845 $O/release_ls_h23_D4628.0000.npz
  date -u "+start %Y-%m-%d %H:%M:%S UTC, k* stage of D 4628 (part A), commit $COMMIT" > $O/run.log
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar 4
  r=$?
  echo "kstar rc $r $(date -u +%H:%M:%S)" >> $O/run.log
  echo "job rc $r $(date -u +%H:%M:%S)" >> $O/run.log
  exit $r
elif [ "$P" = B ]; then
  O=$L/D6666m/tail
  mkdir -p $O/dh610
  get $S/D6666/tail/release_ls.jsonl 1f40daeec0a741d691cc9399001f42105b34efdb $O/dh610/release_ls.jsonl
  get $S/D6666/tail/start.npz 292fe1f0f7d022dc3eac1370c81aebfcf4df3824 $O/dh610/start.npz
  get $S/D6666/tail/release_ls_h15_D6666.0000_step.npz a89b97885355fffd9dc103412e2493324d029655 $O/dh610/release_ls_h15_D6666.0000_step.npz
  date -u "+start %Y-%m-%d %H:%M:%S UTC, D 6666 tail resumed from dh610's h15 step state (part B), commit $COMMIT" > $O/run.log
  cd $HP || exit 1
  PYTHONPATH=$SITE nice -n 10 timeout 16h $PY -u form_s.py release_ls $O/dh610/release_ls_h15_D6666.0000_step.npz $O --harm 15,17,19,21,23 \
    --kmax 23 --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 10 \
    --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls.log 2>&1
  r=$?
  echo "rls h15-h23 rc $r $(date -u +%H:%M:%S)" >> $O/run.log
  [ -s $O/release_ls_h23_D6666.0000.npz ] || { echo "job rc 3 $(date -u +%H:%M:%S)" >> $O/run.log; exit 3; }
  $PY $T/kmax_rule.py $O/release_ls.jsonl > $O/kmax_rule.log 2>&1
  echo "kmax_rule rc $? ($(tail -1 $O/kmax_rule.log))" >> $O/run.log
  HP=$HP SITE=$SITE PY=$PY EXTRA= INNER_CHORD=0 COMMIT=$COMMIT bash $T/kstar_stage.sh $O $O/kstar 10
  r=$?
  echo "kstar rc $r $(date -u +%H:%M:%S)" >> $O/run.log
  echo "job rc $r $(date -u +%H:%M:%S)" >> $O/run.log
  exit $r
fi
echo "usage: d4628k_d6666r_mm5.sh A|B"
exit 1
}
