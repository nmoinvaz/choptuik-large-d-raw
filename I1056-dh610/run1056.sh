#!/bin/bash
# PR #1056 on dh610 (README.md): hp on multishoot 4.1.0, multidouble 5.1.0 and multisolver 0.2.2 (branch chore/multishoot-4.1.0, head e208e136, which also moves
# hp/pyproject.toml's multidouble Python package to 8c4360ac, release 5.1.0, from 482c6835).
# 0. main's hp/src and Cargo pins equal the venv-i1050 build's (empty diff); 1. a worktree and a new venv, pip uninstall multidouble, hp/build.sh (time, peak memory), pip's direct_url
# of multidouble (must name 8c4360ac); 2. venv-i1050: highm_check ref, scaled, jets --save; 3. venv-i1056: the same three --compare against them, and jets --mutate=kappa (must fail);
# 4. venv-i1056 against the stored references (T81, anm-mac) and, added, the kappa control there; 5. the Python helpers: octo_corrector.py planted (#1052's K1 command) on
# venv-i1050 and on venv-i1056, every printed per-step max|F| and the final Delta equal, and --mutate_offset qd on venv-i1056 exits 1.
# One step at a time, nice 10, each under timeout on its exact pid.
. "$(dirname "$0")/common1056.sh"
X=$OUT/exits_1056.txt; S=$OUT/summary_1056.txt
log() { echo "1056 $* $(stamp) UTC" >> $X; }
cd $REPO || exit 1
git fetch -q origin chore/multishoot-4.1.0 || exit 1
HEAD1056=$(git rev-parse origin/chore/multishoot-4.1.0)
[ "$(git rev-parse --short=8 $HEAD1056)" = e208e136 ] || { log "branch head is $HEAD1056, not e208e136: stop"; echo "branch head moved: $HEAD1056" ; exit 1; }
log "start, new build at e208e136 (origin/chore/multishoot-4.1.0), reference build venv-i1050 (worktree $W50 at $(git -C $W50 rev-parse --short=8 HEAD)), load $(cut -d' ' -f1-3 /proc/loadavg)"
# 0. the reference build is main's: main 08699de5 has the same hp/src and pins as 1c02b15b (the venv-i1050 build); the same diff to the PR head must show the pins (its control)
git cat-file -e 08699de5^{commit} || { log "08699de5 missing"; exit 1; }
D0=$(git diff --stat 1c02b15b 08699de5 -- hp/src hp/Cargo.toml hp/Cargo.lock | wc -l)
D1=$(git diff --stat 1c02b15b e208e136 -- hp/Cargo.toml hp/Cargo.lock | tail -1)
echo "# $(stamp) UTC PR #1056 at e208e136 against the venv-i1050 build (worktree $W50 at $(git -C $W50 rev-parse --short=8 HEAD))" > $S
echo "diff 1c02b15b 08699de5 -- hp/src hp/Cargo.toml hp/Cargo.lock: $D0 lines (must be 0) $([ "$D0" = 0 ] && echo OK || echo MISMATCH)" >> $S
echo "control, diff 1c02b15b e208e136 -- hp/Cargo.toml hp/Cargo.lock: $D1 (must be non-empty) $([ -n "$D1" ] && echo OK || echo MISMATCH)" >> $S
echo "hp changes 1c02b15b -> e208e136: $(git diff --stat 1c02b15b e208e136 -- hp | tail -1); files: $(git diff --name-only 1c02b15b e208e136 -- hp | tr '\n' ' ')" >> $S
echo "hp/src changes 1c02b15b -> e208e136: $(git diff --stat 1c02b15b e208e136 -- hp/src | wc -l) lines (must be 0)" >> $S
echo "venv-i1050 build's lock: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $W50/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
echo "pyproject multidouble pin, 1c02b15b: $(git show 1c02b15b:hp/pyproject.toml | grep -o 'multidouble @ [^"]*'); e208e136: $(git show e208e136:hp/pyproject.toml | grep -o 'multidouble @ [^"]*')" >> $S
echo "venv-i1050's installed multidouble package, direct_url: $(cat $V50/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json)" >> $S
[ "$D0" = 0 ] || { log "reference build is not main's: stop"; exit 1; }
[ -d $W ] || git worktree add -q --detach $W $HEAD1056 || exit 1
[ "$(git -C $W rev-parse HEAD)" = $HEAD1056 ] || { echo "WT is not at $HEAD1056"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { echo "worktree not clean"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
# runin NAME WANT CAP cmd...: from $W/hp, log to $OUT/NAME.log, a summary line with the exit, wall seconds and the rows counted
runin() { local name=$1 want=$2 cap=$3; shift 3; cd $W/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s), bit-identical rows $(grep -cE '^  M = .*bit-identical' $OUT/$name.log), DIFFERS rows $(grep -cE '^  M = .*DIFFERS' $OUT/$name.log); last: $(grep -vE '^exit ' $OUT/$name.log | tail -1 | cut -c1-120) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
# 1. venv, the multidouble package out, build (without pip's cache, so that no cached wheel of another commit is reused)
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $W/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
export PIP_NO_CACHE_DIR=1
python -m pip uninstall -y multidouble >> $OUT/venv.log 2>&1
echo "# python $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), lock of e208e136: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $W/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
echo "venv-i1056 before the build: multidouble package $(python -m pip show multidouble 2>&1 | head -1)" >> $S
runin build1056 0 5580 bash build.sh
echo "build1056 peak memory of the unit so far (venv and build): $(( $(systemctl --user show $UNIT -p MemoryPeak | cut -d= -f2) / 1048576 )) MiB" >> $S
DU=$(cat $VENV/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>&1)
echo "venv-i1056's installed multidouble package, direct_url: $DU; names 8c4360ac: $(case "$DU" in *8c4360ac*) echo OK;; *) echo MISMATCH;; esac)" >> $S
for V in $V50 $VENV; do echo "hpkernel import $V: $($V/bin/python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), hpkernel.__file__, 'multidouble', multidouble.isa())" 2>&1 | tail -1)" >> $S; done
PY50=$V50/bin/python; PY56=$VENV/bin/python
R=$RAW/T81; J=$RAW/anm-mac/jets_inputs/jets_inputs.json
# 2. the reference build (venv-i1050) saves (est. 1, 8, 2 min)
runin save_ref 0 1800 $PY50 highm_check.py ref --save=$OUT/REF.json --Ms=48,64,80
runin save_scaled 0 7200 $PY50 highm_check.py scaled --save=$OUT/SC.json
runin save_jets 0 1800 $PY50 highm_check.py jets --save=$OUT/JETS.json
# 3. the new build (venv-i1056) compares with them; the kappa control must fail
runin cmp_ref 0 1800 $PY56 highm_check.py ref --compare=$OUT/REF.json --Ms=48,64,80
runin cmp_scaled 0 7200 $PY56 highm_check.py scaled --compare=$OUT/SC.json
runin cmp_jets 0 1800 $PY56 highm_check.py jets --compare=$OUT/JETS.json
runin cmp_jets_kappa 1 1800 $PY56 highm_check.py jets --compare=$OUT/JETS.json --mutate=kappa
# 4. the new build against the stored references; the kappa control there is added (it is cheap and the stored inputs are a different path)
runin stored_ref 0 1800 $PY56 highm_check.py ref --compare=$R/ref_main.json --Ms=48,64,80
runin stored_scaled 0 7200 $PY56 highm_check.py scaled --compare=$R/scaled_main.json
runin stored_jets 0 1800 $PY56 highm_check.py jets --compare=$J
runin stored_jets_kappa 1 1800 $PY56 highm_check.py jets --compare=$J --mutate=kappa
# 5. the Python helpers (octo_corrector.py: od_axpy, od_add_dd from the multidouble package), which highm_check does not reach: #1052's K1 command, est. 4 min a run
P=T129-win2/chain/anm_pin3_D180.5246.npz
runin planted_i1050 0 5400 $PY50 -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --out $OUT/planted_i1050
runin planted_i1056 0 5400 $PY56 -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --out $OUT/planted_i1056
runin planted_i1056_mut_offset_qd 1 5400 $PY56 -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --mutate_offset qd --out $OUT/planted_i1056_mut_offset_qd
cd $OUT
python3 cmp_planted.py planted_i1050.log planted_i1056.log > cmp_planted.txt 2>&1; r1=$?
python3 cmp_planted.py planted_i1050.log planted_i1056.log --mutate > cmp_planted_control.txt 2>&1; r2=$?
python3 cmp_planted.py planted_i1056.log planted_i1056_mut_offset_qd.log > cmp_planted_offset.txt 2>&1; r3=$?
CMPNP="import numpy as np,sys;a,b=(np.load(f) for f in sys.argv[1:]);k=['zh','zl','z2','z3','z4','z5','z6','z7'];ok=all(np.array_equal(a[x],b[x]) for x in k);print('bit for bit' if ok else 'DIFFER');sys.exit(not ok)"
$PY56 -c "$CMPNP" planted_i1050.npz planted_i1056.npz > cmp_planted_npz.txt 2>&1; r4=$?
echo "planted logs, venv-i1050 against venv-i1056: exit $r1 (0: every printed digit equal): $(tail -1 cmp_planted.txt); comparator control (--mutate) exit $r2 (1): $(tail -1 cmp_planted_control.txt | cut -c1-100); venv-i1056's base against its --mutate_offset qd run: exit $r3 (1 expected, the logs differ): $(tail -1 cmp_planted_offset.txt | cut -c1-100); final states npz: exit $r4: $(cat cmp_planted_npz.txt)" >> $S
log "planted compare exit $r1 control $r2 offset $r3 npz $r4"
log "all steps done"
