#!/bin/bash
# #1098 on dh370 (coordinator, 2026-11-27): D 5555's M 32 stages resumed after ladder_point2.sh's 6 h limit on
# rls h5-h11 ended them at 09:16:15 UTC (rc 124; h5 released, h7's outer step 0 accepted and saved). release_ls from
# that step state (rls/release_ls_h7_D5555.0000_step.npz; --harm 7 from it resumes, the held values being read from the
# state) for h7, h9 and h11 into rls_b, then h13 into rls13, with ladder_point2.sh's (e0cf5880) options and the time
# limits raised to 16 h and 10 h. The Python copy, site, interpreter and commit of d5555_370.sh. It ends after rls13
# (STOP_AFTER rls13) and writes "job rc N" to run.log, as the first job did.
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=/home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh370/ladder/D5555
HP=$W/hp_y5555; SITE=$W/site_sky; PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python; COMMIT=f398e829
S7=$O/rls/release_ls_h7_D5555.0000_step.npz
done_rc() { echo "job rc $1 $(date -u +%H:%M:%S)" >> $O/run.log; exit $1; }
cd $HP || done_rc 1
grep -q "floor_dz=1e-12" form_s.py || done_rc 1
[ -s $S7 ] || done_rc 2
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
echo "resume $(date -u '+%Y-%m-%d %H:%M:%S UTC') from rls/release_ls_h7_D5555.0000_step.npz (blob $(git hash-object --no-filters $S7)), d5555_resume_370.sh" >> $O/run.log
mkdir -p $O/rls_b $O/rls13
nice -n 10 timeout 16h $PY -u form_s.py release_ls $S7 $O/rls_b --harm 7,9,11 --kmax 13 --jac qd --res od --tol 1e-36 \
  --tol_h 1e-30 --ddelta 1 --threads 6 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls_b/rls.log 2>&1
echo "rls_b h7-h11 rc $? $(date -u +%H:%M:%S)" >> $O/run.log
R=$O/rls_b/release_ls_h11_D5555.0000.npz
[ -s $R ] || done_rc 3
nice -n 10 timeout 10h $PY -u form_s.py release_ls $R $O/rls13 --harm 13 --kmax 13 --jac qd --res od --tol 1e-48 \
  --tol_h 1e-44 --ddelta 1e-25 --threads 6 --outer 8 --inner_chord 0 --commit $COMMIT > $O/rls13/rls.log 2>&1
echo "rls h13 rc $? $(date -u +%H:%M:%S)" >> $O/run.log
[ -s $O/rls13/release_ls_h13_D5555.0000.npz ] || done_rc 4
echo "stopped after rls13 (STOP_AFTER) $(date -u +%H:%M:%S)" >> $O/run.log
done_rc 0
}
