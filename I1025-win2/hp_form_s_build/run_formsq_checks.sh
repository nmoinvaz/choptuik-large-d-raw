#!/bin/bash
# win2: the form-S selftests after the hp build of origin/wip/large-d-form-s (D:\choptuik-formsq, venv-formsq): waits for build.done, refuses unless the build exited 0,
# stops the commit sampler, then runs (from D:\choptuik-formsq\hp, BelowNormal): floor_stop_check.py (0), --stale (0), --mutate=nofloor (must be non-zero),
# form_s.py check on the stored state inputs/anm_pin3_D80.5157.npz (blob 2d90f119), and the same with --mutate flux (the control: it must move Delta).
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/hp_form_s_build
WT=/d/choptuik-formsq
V=/c/Users/nathan/Source/venv-formsq
PY=$V/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-formsq PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
EX=$OUT/checks_exits.txt
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a "$EX"; }
until [ -e "$OUT/build.done" ]; do sleep 30; done
rc=$(grep -E '^end .* exit [0-9]+' "$OUT/build.times" | tail -1 | sed 's/.* exit //')
touch "$OUT/commit_watch.stop"
say "checks: the build ended with exit ${rc:-?}"
[ "${rc:-1}" = 0 ] || { say "checks: STOP, the build did not exit 0, no selftest run"; exit 2; }
h=$(git hash-object --no-filters "$OUT/inputs/anm_pin3_D80.5157.npz"); case "$h" in 2d90f119*) ;; *) say "checks: STOP, the state is blob $h, not 2d90f119"; exit 2;; esac
cd "$WT/hp" || exit 1
say "worktree commit $(git -C $WT rev-parse HEAD | cut -c1-12); $("$PY" -I -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.isa(), "multidouble", multidouble.isa())' 2>&1 | tail -1)"
mkdir -p "$OUT/checks"
run() {  # NAME WANT CMD...  (WANT: 0, or nz for non-zero)
  local n=$1 want=$2; shift 2
  local t0=$(date +%s)
  "$@" > "$OUT/checks/$n.log" 2>&1; local r=$?
  local ok=FAIL; { [ "$want" = 0 ] && [ $r = 0 ]; } || { [ "$want" = nz ] && [ $r != 0 ]; } && ok=OK
  say "check $n: exit $r (want $want) $ok, $(( $(date +%s) - t0 )) s: $(grep -E 'PASS|FAIL|converged|Delta_S' "$OUT/checks/$n.log" | tail -2 | tr '\n' ' ' | cut -c1-300)"
}
run floor_stop            0  "$PY" -I floor_stop_check.py
run floor_stop_stale      0  "$PY" -I floor_stop_check.py --stale
run floor_stop_nofloor    nz "$PY" -I floor_stop_check.py --mutate=nofloor
run form_s_check          0  "$PY" -I form_s.py check "$OUT/inputs/anm_pin3_D80.5157.npz" --threads 2
run form_s_check_flux     0  "$PY" -I form_s.py check "$OUT/inputs/anm_pin3_D80.5157.npz" --threads 2 --mutate flux
say "checks: all five ran (see checks/*.log); the Delta readings are in the two form_s_check logs"
touch "$OUT/checks.done"
exit 0
