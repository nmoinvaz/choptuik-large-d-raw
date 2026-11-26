#!/bin/bash
# #1098, D 622's bound at k* = 15: its tail released h15 at the kfree-15 system's |F| 3.41e-51 (the inner solve stopped
# just below tol 1e-48), so gain (1.05e28) x |F| bounds Delta only to 3.6e-23. This re-converges that system from the h15
# state (raw I1098-mm5/ladder/D622/tail/release_ls_h15_D622.0000.npz, blob 7209f398) to tol 1e-62: release_ls --harm 15
# --kmax 15 (the target system is kfreeze 15, as gainq.py's), qq, od, 4 threads, on fastmul6 (site_y), into this raw
# worktree's I1098-dh610/reconv622/, then commits and pushes it
{
W=/home/nathan/Source/choptuik-large-d-1088a
WT=/home/nathan/Source/choptuik-large-d-raw-1088a
O=$WT/I1098-dh610/reconv622
mkdir -p $O
cd $WT || exit 1
git fetch -q origin || exit 2
git cat-file blob 7209f3989026c15f401a8c2242eb9f7d00f1f044 > $O/h15_D622.npz || exit 3
cd $W/hp_y || exit 4
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
PY=$(cat $W/python_path)
cp $W/reconv622.sh $O/
{
  echo "# I1098-dh610/reconv622: D 622's kfree-15 system re-converged from its h15 state (#1098)"
  echo
  echo "Machine: dh610 (Fedora, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098"
  echo
  echo "D 622's tail released h15 at the kfree-15 system's |F| 3.41e-51, so the gain at kfreeze 15 (1.05e28, gainq.py on the"
  echo "final state) times |F| bounds Delta only to 3.6e-23. \`reconv622.sh\` re-converges that system from the h15 state"
  echo "(I1098-mm5/ladder/D622/tail/release_ls_h15_D622.0000.npz, blob 7209f398, copied here as h15_D622.npz) to tol 1e-62"
  echo "by release_ls --harm 15 --kmax 15 (qq Jacobian, octo-double residual, 4 threads, fastmul6 site_y). Its last target"
  echo "|F| and its change of Delta from the h15 state give D 622's err_resid."
} > $O/README.md
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
nice -n 10 timeout 3h $PY -u form_s.py release_ls $O/h15_D622.npz $O --harm 15 --kmax 15 --jac qq --res od --tol 1e-62 \
  --tol_h 1e-50 --ddelta 1e-40 --threads 4 --outer 4 --inner_chord 0 --commit 478e9d86 > $O/rls.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/run.log
cd $WT || exit 5
python3 make_index.py > /dev/null
git add I1098-dh610/reconv622 INDEX.md
git commit -qm "I1098-dh610/reconv622: D 622's kfree-15 system re-converged from its h15 state to tol 1e-62"
for i in 1 2 3 4 5; do git pull -q --rebase origin main && git push -q origin HEAD:main && break; sleep 60; done
git rev-parse --short=9 HEAD >> $W/out/reconv622.commit
exit
}
