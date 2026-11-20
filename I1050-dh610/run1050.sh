#!/bin/bash
# PR #1050 on dh610 (README.md): new worktree at the branch head, new venv, hp/build.sh, #1034's step 5 commands unchanged, and the row-by-row comparison with the 9980cd93 build's step 5 logs.
. "$(dirname "$0")/common1050.sh"
X=$OUT/exits_1050.txt; S=$OUT/summary_1050.txt
log() { echo "1050 $* $(stamp) UTC" >> $X; }
cd $REPO || exit 1
git fetch -q origin || exit 1
HEAD1050=$(git rev-parse origin/chore/multishoot-4.0.0)
[ -d $WT ] || git worktree add -q --detach $WT $HEAD1050 || exit 1
[ "$(git -C $WT rev-parse HEAD)" = $HEAD1050 ] || { echo "WT is not at the branch head $HEAD1050"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "worktree not clean"; exit 1; }
log "start, new build at $(git -C $WT rev-parse --short=8 HEAD) (origin/chore/multishoot-4.0.0), old build 9980cd93 (I1034-dh610), load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC hp new $(git -C $WT rev-parse --short=8 HEAD) against old 9980cd93; hp diff: $(git -C $WT diff --stat 9980cd93 HEAD -- hp | tail -1)" > $S
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
runin() { local name=$1 want=$2 cap=$3; shift 3; cd $WT/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $WT/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
echo "# python $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), lock: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $WT/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
runin build1050 0 5580 bash build.sh
python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), hpkernel.__file__, 'multidouble', multidouble.isa())" > $OUT/hpkernel_import.log 2>&1; echo "hpkernel import: exit $? $(tail -1 $OUT/hpkernel_import.log)" >> $S
runin step5_ref 0 1800 python3 highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
runin step5_scaled 0 7200 python3 highm_check.py scaled --compare=$RAW/T81/scaled_main.json
runin step5_jets 0 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
runin step5_jets_kappa 1 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
cd $OUT
for f in step5_ref step5_scaled step5_jets step5_jets_kappa; do
  python3 compare1050.py $OLD/$f.log $OUT/$f.log > $OUT/compare_$f.txt; r1=$?
  python3 compare1050.py $OLD/$f.log $OUT/$f.log --mutate > $OUT/compare_${f}_control.txt; r2=$?
  echo "compare $f: exit $r1 (0: bit-identical rows), control --mutate exit $r2 (1): $(tail -1 $OUT/compare_$f.txt | cut -c1-200)" >> $S; log "compare $f exit $r1 control $r2"
done
log "all steps done"
