#!/bin/bash
# PR #1055 on dh610 (README.md): the Linux checks of --plan_auto (Taylor order by planned cost), branch perf/plan-auto, head 2928d458, rebased onto main 4ac62582.
# 0. venv-i1056 (e208e136) is main's build: main 4ac62582's hp/src and pins against e208e136; 1. a worktree at 2928d458, a new venv (venv-i1055), pip uninstall multidouble, hp/build.sh (time, peak memory);
# 2. flag off: highm_check ref --Ms=48,64,80, scaled, jets, --save on venv-i1056, --compare on venv-i1055, and jets --mutate=kappa (must fail);
# 3. from the worktree's hp/: plan_auto_gain.py planted --check (and its control --mutate n, which must fail; selftest added), cargo test --profile release-dev --lib plan_auto -- --nocapture.
# One step at a time, nice 10, each under timeout on its exact pid.
. "$(dirname "$0")/common1055.sh"
X=$OUT/exits_1055.txt; S=$OUT/summary_1055.txt
log() { echo "1055 $* $(stamp) UTC" >> $X; }
cd $REPO || exit 1
git fetch -q origin perf/plan-auto main || exit 1
HEAD1055=$(git rev-parse origin/perf/plan-auto)
[ "$(git rev-parse --short=8 $HEAD1055)" = 2928d458 ] || { log "branch head is $HEAD1055, not 2928d458: stop"; echo "branch head moved: $HEAD1055"; exit 1; }
[ "$(git -C $W56 rev-parse --short=8 HEAD)" = e208e136 ] || { log "$W56 is not at e208e136: stop"; exit 1; }
log "start, new build at 2928d458 (origin/perf/plan-auto), reference build venv-i1056 (worktree $W56 at $(git -C $W56 rev-parse --short=8 HEAD)), load $(cut -d' ' -f1-3 /proc/loadavg)"
# 0. main's hp/src and pins against the venv-i1056 build (the coordinator's command, which it expected to be empty), and the controls
D0=$(git diff --stat e208e136 4ac62582 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml)
F0=$(git diff --name-only e208e136 4ac62582 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml | tr '\n' ' ')
echo "# $(stamp) UTC PR #1055 at 2928d458 against the venv-i1056 build (worktree $W56 at e208e136), main 4ac62582" > $S
echo "diff --stat e208e136 4ac62582 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml: files [ $F0] ($(echo "$D0" | tail -1 | sed 's/^ *//'))" >> $S
echo "split_tests is declared in 4ac62582's hp/src/lib.rs as: $(git show 4ac62582:hp/src/lib.rs | grep -B1 'mod split_tests' | tr '\n' ' ')" >> $S
echo "merge base of 4ac62582 and 2928d458: $(git merge-base 4ac62582 2928d458 | cut -c1-8); the PR's files against it: $(git diff --name-only 4ac62582 2928d458 | tr '\n' ' ')" >> $S
echo "control, diff --name-only e208e136 2928d458 -- hp/src: $(git diff --name-only e208e136 2928d458 -- hp/src | tr '\n' ' ') (must list plan_auto.rs)" >> $S
echo "pyproject multidouble pin, e208e136: $(git show e208e136:hp/pyproject.toml | grep -o 'multidouble @ [^"]*' | cut -c1-80); 2928d458: $(git show 2928d458:hp/pyproject.toml | grep -o 'multidouble @ [^"]*' | cut -c1-80)" >> $S
echo "Cargo pins, e208e136: $(git show e208e136:hp/Cargo.toml | grep -E '^(multishoot|multisolver|multidouble) ' | cut -c1-40 | tr '\n' ';'); 2928d458: $(git show 2928d458:hp/Cargo.toml | grep -E '^(multishoot|multisolver|multidouble) ' | cut -c1-40 | tr '\n' ';')" >> $S
echo "venv-i1056's installed multidouble package, direct_url: $(cat $V56/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json)" >> $S
# the build is main's unless a file other than the cfg(test) module split_tests.rs differs
case "$F0" in ""|"hp/src/split_tests.rs ") ;; *) log "files beyond split_tests.rs differ ($F0): stop"; exit 1;; esac
[ -d $W ] || git worktree add -q --detach $W $HEAD1055 || exit 1
[ "$(git -C $W rev-parse HEAD)" = $HEAD1055 ] || { echo "WT is not at $HEAD1055"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { echo "worktree not clean"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
runin() { local name=$1 want=$2 cap=$3; shift 3; cd $W/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s), bit-identical rows $(grep -cE '^  M = .*bit-identical' $OUT/$name.log), DIFFERS rows $(grep -cE '^  M = .*DIFFERS' $OUT/$name.log); last: $(grep -vE '^exit ' $OUT/$name.log | tail -1 | cut -c1-120) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
# 1. venv, the multidouble package out, build (without pip's cache)
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $W/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
export PIP_NO_CACHE_DIR=1
python -m pip uninstall -y multidouble >> $OUT/venv.log 2>&1
echo "# python $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), lock of 2928d458: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $W/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
echo "venv-i1055 before the build: multidouble package $(python -m pip show multidouble 2>&1 | head -1)" >> $S
runin build1055 0 5580 bash build.sh
echo "build1055 peak memory of the unit so far (venv and build): $(( $(systemctl --user show $UNIT -p MemoryPeak | cut -d= -f2) / 1048576 )) MiB" >> $S
DU=$(cat $VENV/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>&1)
echo "venv-i1055's installed multidouble package, direct_url: $DU; names 8c4360ac: $(case "$DU" in *8c4360ac*) echo OK;; *) echo MISMATCH;; esac)" >> $S
for V in $V56 $VENV; do echo "hpkernel import $V: $($V/bin/python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), hpkernel.__file__, 'multidouble', multidouble.isa(), 'has Solver.plan_auto', hasattr(hpkernel.Solver, 'plan_auto'))" 2>&1 | tail -1)" >> $S; done
PYM=$V56/bin/python; PYN=$VENV/bin/python
# 2. flag off: the references saved with venv-i1056 (main's build), compared by venv-i1055 (est. 1, 6, 1.5 min a run)
runin save_ref 0 1800 $PYM highm_check.py ref --save=$OUT/REF.json --Ms=48,64,80
runin save_scaled 0 7200 $PYM highm_check.py scaled --save=$OUT/SC.json
runin save_jets 0 1800 $PYM highm_check.py jets --save=$OUT/JETS.json
runin cmp_ref 0 1800 $PYN highm_check.py ref --compare=$OUT/REF.json --Ms=48,64,80
runin cmp_scaled 0 7200 $PYN highm_check.py scaled --compare=$OUT/SC.json
runin cmp_jets 0 1800 $PYN highm_check.py jets --compare=$OUT/JETS.json
runin cmp_jets_kappa 1 1800 $PYN highm_check.py jets --compare=$OUT/JETS.json --mutate=kappa
# 3. the PR's planted truth (no kernel, seconds), its control (--mutate n), the report's selftest (added: run 0 of the note), then the Rust checks
runin planted 0 1800 $PYN plan_auto_gain.py planted --check data/plan_auto/planted.txt
runin planted_control_n 1 1800 $PYN plan_auto_gain.py planted --check data/plan_auto/planted.txt --mutate n
runin selftest 0 1800 $PYN plan_auto_gain.py selftest
runin cargo_test_plan_auto 0 7200 cargo test --profile release-dev --lib plan_auto -- --nocapture
echo "cargo test: $(grep -E '^test |^test result' $OUT/cargo_test_plan_auto.log | tr '\n' ';' | cut -c1-900)" >> $S
echo "unit memory peak at the end: $(( $(systemctl --user show $UNIT -p MemoryPeak | cut -d= -f2) / 1048576 )) MiB" >> $S
log "all steps done"
