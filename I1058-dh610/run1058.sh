#!/bin/bash
# #1058 on dh610 (README.md): hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0, Python package 8c4360ac) in a new worktree and a new venv, then the four
# stored-reference checks from hp/. A braced block ending in exit; one step at a time, nice 10, each check under timeout.
{
. "$(dirname "$0")/common1058.sh"
X=$OUT/exits_1058.txt; S=$OUT/summary_1058.txt
log() { echo "1058 $* $(stamp) UTC" >> $X; }
cd $REPO || exit 1
git fetch -q origin main || exit 1
M=$(git rev-parse 8179068d^{commit}) || exit 1
[ "$(git rev-parse --short=8 $M)" = 8179068d ] || { log "8179068d resolves to $M: stop"; exit 1; }
git merge-base --is-ancestor $M origin/main || { log "$M is not on origin/main: stop"; exit 1; }
log "start, main $M (origin/main is $(git rev-parse --short=8 origin/main)), load $(cut -d' ' -f1-3 /proc/loadavg)"
[ -d $W ] || git worktree add -q --detach $W $M || exit 1
[ "$(git -C $W rev-parse HEAD)" = $M ] || { log "worktree $W is not at $M: stop"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { log "worktree $W not clean: stop"; exit 1; }
echo "# $(stamp) UTC #1058 on dh610 at main $M, worktree $W, venv $VENV" > $S
echo "lock of $W: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $W/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
echo "pyproject multidouble pin: $(grep -o 'multidouble @ [^"]*' $W/hp/pyproject.toml)" >> $S
echo "hp/src last changed at $(git log -1 --format=%h $M -- hp/src)" >> $S
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
# runin NAME WANT CAP cmd...: from $W/hp, log to $OUT/NAME.log, a summary line with the exit, wall seconds and the rows counted
runin() { local name=$1 want=$2 cap=$3; shift 3; cd $W/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s); last: $(grep -vE '^exit ' $OUT/$name.log | tail -1 | cut -c1-140) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
# 1. a new venv, the multidouble package out, the build (no pip cache, so that no cached wheel of another commit is reused)
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $W/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
export PIP_NO_CACHE_DIR=1
echo "venv-i1058 before the uninstall: multidouble package $(python -m pip show multidouble 2>&1 | head -2 | tr '\n' ' ')" >> $S
python -m pip uninstall -y multidouble >> $OUT/venv.log 2>&1
echo "venv-i1058 after the uninstall: $(python -m pip show multidouble 2>&1 | head -1)" >> $S
echo "# python $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), $(rustc --version 2>&1)" >> $S
runin build1058 0 5580 bash build.sh
echo "build1058 peak memory of the unit so far (the venv and the build): $(( $(systemctl --user show $UNIT -p MemoryPeak | cut -d= -f2) / 1048576 )) MiB" >> $S
DU=$(cat $VENV/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>&1)
echo "venv-i1058's installed multidouble package, direct_url: $DU; names 8c4360ac: $(case "$DU" in *8c4360ac*) echo OK;; *) echo MISMATCH;; esac)" >> $S
DU50=$(cat $V50/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>&1)
echo "control, venv-i1050's package (482c6835) read by the same test: names 8c4360ac: $(case "$DU50" in *8c4360ac*) echo MISMATCH;; *) echo OK, it does not;; esac)" >> $S
PROBE="import hpkernel, multidouble; S=hpkernel.Solver; print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa(), 'set_exact_recip', hasattr(S,'set_exact_recip'), 'plan_auto', hasattr(S,'plan_auto'), hpkernel.__file__)"
for V in $VENV $V54 $V56; do echo "import $V: $($V/bin/python -c "$PROBE" 2>&1 | tail -1)" >> $S; done
echo "venv-i1058's _hpkernel .so sha1: $(sha1sum $VENV/lib/python3.14/site-packages/hpkernel/*.so | cut -c1-12)" >> $S
# 2. the four stored-reference checks, from hp/ (pass: 0 differing rows; the kappa control must fail)
PYN=$VENV/bin/python; R=$RAW/T81; J=$RAW/anm-mac/jets_inputs/jets_inputs.json
runin check_ref 0 1800 $PYN highm_check.py ref --compare=$R/ref_main.json --Ms=48,64,80
runin check_scaled 0 7200 $PYN highm_check.py scaled --compare=$R/scaled_main.json
runin check_jets 0 1800 $PYN highm_check.py jets --compare=$J
runin check_jets_kappa 1 1800 $PYN highm_check.py jets --compare=$J --mutate=kappa
for N in ref scaled jets jets_kappa; do echo "check_$N: rows 'bit-identical' $(grep -cE 'bit-identical' $OUT/check_$N.log), DIFFERS $(grep -cE 'DIFFERS' $OUT/check_$N.log)" >> $S; done
echo "stored files sha1: $(sha1sum $R/ref_main.json $R/scaled_main.json $J | cut -c1-12 | tr '\n' ' ')" >> $S
echo "peak memory of the unit after the checks: $(( $(systemctl --user show $UNIT -p MemoryPeak | cut -d= -f2) / 1048576 )) MiB" >> $S
log "all steps done"
exit
}
