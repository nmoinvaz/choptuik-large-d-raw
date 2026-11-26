#!/bin/bash
# #1098, D 747's k* stage on dh610: its tail's log and its h15 and h23 states (raw I1098-mm5/ladder/D747/tail at
# 22e5900aa or later) and the k* tools (I1098-mac-a/tools) written from raw into dh610's sparse raw worktree's
# I1098-dh610/kstar747/, then kstar_stage.sh there (fastmul6 site_y, 6 threads, chord-free), then a commit and push
{
W=/home/nathan/Source/choptuik-large-d-1088a
WT=/home/nathan/Source/choptuik-large-d-raw-1088a
T=$WT/I1098-dh610/kstar747
cd $WT || exit 1
git pull -q --rebase origin main || exit 2
mkdir -p $T/tail $T/tools
for f in release_ls.jsonl release_ls_h15_D747.0000.npz release_ls_h23_D747.0000.npz; do
  git show origin/main:I1098-mm5/ladder/D747/tail/$f > $T/tail/$f || exit 3
done
for f in kstar_stage.sh kstar_gain.py kstar_summary.py; do
  git show origin/main:I1098-mac-a/tools/$f > $T/tools/$f || exit 3
done
[ "$(git hash-object --no-filters $T/tail/release_ls_h23_D747.0000.npz | cut -c1-8)" = "a64b0964" ] || exit 4
HP=$W/hp_y SITE=$W/site_y PY=$(cat $W/python_path) COMMIT=478e9d86 INNER_CHORD=0 nice -n 10 bash $T/tools/kstar_stage.sh $T/tail $T/kstar 6
echo "kstar_stage rc $? $(date -u +%H:%M:%S)" >> $T/kstar/run.log
cp $W/kstar747.sh $T/
python3 make_index.py > /dev/null
git add I1098-dh610/kstar747 INDEX.md
git commit -qm "I1098-dh610/kstar747: D 747's k* stage (kfree 15) from its M 48 tail" || exit 5
for i in 1 2 3; do git pull -q --rebase origin main && git push -q origin HEAD:main && break; sleep 30; done
git log --oneline -1 > $W/out/kstar747.commit
exit
}
