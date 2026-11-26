#!/bin/bash
# #1098, D 2000: its M 48 tail (out/fix6/D2000_M48_6b, stopped by pid at 22:32 UTC after h25's release, by the kmax 23
# rule) copied into dh610's sparse raw worktree (I1098-dh610/fix6/D2000_M48_6b), then its k* stage there (kstar_stage.sh,
# fastmul6 site_y, 8 threads), then a commit and push
{
W=/home/nathan/Source/choptuik-large-d-1088a
WT=/home/nathan/Source/choptuik-large-d-raw-1088a
T=$WT/I1098-dh610/fix6/D2000_M48_6b
cd $WT || exit 1
git pull -q --rebase origin main || exit 2
mkdir -p $T $WT/I1098-dh610/kstar2000/tools
cp -a $W/out/fix6/D2000_M48_6b/. $T/
cp $W/run_m48_2000_6b.sh $W/kstar2000.sh $T/
for f in kstar_stage.sh kstar_gain.py kstar_summary.py kmax_rule.py; do
  git show origin/main:I1098-mac-a/tools/$f > $WT/I1098-dh610/kstar2000/tools/$f || exit 3
done
python3 $WT/I1098-dh610/kstar2000/tools/kmax_rule.py $T/release_ls.jsonl > $T/kmax_rule.log 2>&1
HP=$W/hp_y SITE=$W/site_y PY=$(cat $W/python_path) COMMIT=478e9d86 INNER_CHORD=0 nice -n 10 \
  bash $WT/I1098-dh610/kstar2000/tools/kstar_stage.sh $T $T/kstar 8
echo "kstar_stage rc $? $(date -u +%H:%M:%S)" >> $T/kstar/run.log
python3 make_index.py > /dev/null
git add I1098-dh610/fix6/D2000_M48_6b I1098-dh610/kstar2000 INDEX.md
git commit -qm "I1098-dh610/fix6/D2000_M48_6b: D 2000's M 48 tail to h25 (kmax 23 rule) and its k* stage" || exit 5
for i in 1 2 3; do git pull -q --rebase origin main && git push -q origin HEAD:main && break; sleep 30; done
git log --oneline -1 > $W/out/kstar2000.commit
exit
}
