#!/bin/bash
# #1098, D 622's machine check on dh170, after unit i1088a-r1549c (D 1549's h13) ends, at most 10 h: mm5's D 622 tail
# stage again, bit for bit in its inputs: release_ls from mm5's tail input (I1098-mm5/ladder/D622/tail/h13_M48.npz, blob
# 98479d80) with ladder_point2.sh's tail options (--harm 13..23, kmax 23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25,
# outer 8, 6 threads), no variant_state step, on the Skylake fastmul6 wheel (site_sky, Python f398e829) with
# --inner_chord 0. Output into the live raw worktree's I1098-dh170/ladder/D622x (no --allow_unraw). Bar: the final state
# equal to mm5's (blob 042eaacf), or within 1e-25 in Delta of 1.660501812395454452123410593519465372918
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh170/ladder/inputs
O=$LV/I1098-dh170/ladder/D622x
n=0
while [ $n -lt 1800 ]; do systemctl --user is-active --quiet i1088a-r1549c || break; sleep 20; n=$((n + 1)); done
systemctl --user is-active --quiet i1088a-r1549c && exit 1
mkdir -p $I $O
cd $LV || exit 2
git fetch -q origin || exit 2
git cat-file blob 98479d80fdec26a6eff3811c83a04383cd79394d > $I/D622_tail_h13_M48.npz || exit 2
[ "$(git hash-object --no-filters $I/D622_tail_h13_M48.npz)" = "98479d80fdec26a6eff3811c83a04383cd79394d" ] || exit 2
cd $W/hp_y || exit 3
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_sky
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
nice -n 10 timeout 10h $PY -u form_s.py release_ls $I/D622_tail_h13_M48.npz $O --harm 13,15,17,19,21,23 --kmax 23 \
  --jac_by 13:qq,15:qq,17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 6 --outer 8 \
  --inner_chord 0 --commit f398e829 > $O/rls.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/run.log
cp $W/d622x_170.sh $O/
echo "final state blob $(git -C $LV hash-object --no-filters $O/release_ls_h23_D622.0000.npz 2>/dev/null) (mm5's 042eaacf)" >> $O/run.log
echo "job rc 0 $(date -u +%H:%M:%S)" >> $O/run.log
exit
}
