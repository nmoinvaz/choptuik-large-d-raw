#!/bin/bash
# I1088-win2/L8000 on win2 (the coordinator's order of 2026-11-26 ~01:30 UTC, #1088): D 8000 held at L = 20, direct solve, from the build worktree D:\choptuik-formsq.
# Waits for the form-S selftests (hp_form_s_build/checks.done), reads them with checks_gate.py (registered readings), checks out origin/wip/large-d-form-s at 4f5eaf69
# (Python files only since the build's ab2446b8: checked by diff), then runs `form_s_lastnode.py solvestate` from hp/ with OPENBLAS_NUM_THREADS=2, BelowNormal
# (started through cim_start.ps1), cap 8 h by the exact root pid (crun). usage: run_L8000.sh   (DRY=1: the checks of the pins and the gate selftest only)
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
RAW=/d/choptuik-i935-raw; WRAW=D:/choptuik-i935-raw
OUT=$RAW/I1088-win2/L8000; WOUT=$WRAW/I1088-win2/L8000
BUILD=$RAW/I1025-win2/hp_form_s_build
WT=/d/choptuik-formsq
V=/c/Users/nathan/Source/venv-formsq; PY=$V/Scripts/python.exe
CAP=28800
COMMIT=4f5eaf69
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-formsq PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=2
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a "$OUT/L8000_events.txt"; }
refuse() { say "L8000 STOP: $*"; echo "$*" > "$OUT/L8000_refused.txt"; exit ${2:-2}; }
mkdir -p "$OUT"
[ -e "$OUT/L8000.done" ] && { echo "refuse: L8000.done exists"; exit 2; }
h=$(git hash-object --no-filters "$OUT/guess_D8000.0000.npz"); case "$h" in 2c59ff47*) ;; *) refuse "the guess is blob $h, not 2c59ff47";; esac
h=$(git hash-object --no-filters "$OUT/checks_gate.py"); say "checks_gate.py blob $h"
"$PY" -I "$OUT/checks_gate.py" --selftest > "$OUT/gate_selftest.txt" 2>&1; g0=$?
"$PY" -I "$OUT/checks_gate.py" --selftest --mutate > "$OUT/gate_selftest_mutate.txt" 2>&1; g1=$?
[ "$g0 $g1" = "0 1" ] || refuse "the gate's selftests did not behave (plain $g0, --mutate $g1; wanted 0 1)"
say "gate selftests ok (0 1); the guess is blob 2c59ff47; waiting for the form-S selftests"
[ "${DRY:-0}" = 1 ] && exit 0
until [ -e "$BUILD/checks.done" ] || { [ -e "$BUILD/checks_exits.txt" ] && grep -q "STOP" "$BUILD/checks_exits.txt"; }; do sleep 30; done
[ -e "$BUILD/checks.done" ] || refuse "the build or its selftests stopped before they ran (see hp_form_s_build/checks_exits.txt)"
"$PY" -I "$OUT/checks_gate.py" "$BUILD" > "$OUT/gate_reading.txt" 2>&1; gr=$?
cat "$OUT/gate_reading.txt" | while read l; do say "gate: $l"; done
[ $gr = 0 ] || refuse "the form-S selftests did not read as registered (gate_reading.txt): D 8000 not started" 3
cd "$WT" || exit 1
git diff --quiet ab2446b8 $COMMIT -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/build.sh || refuse "hp/src or the Cargo files differ between ab2446b8 and $COMMIT: the built hpkernel does not match"
git fetch origin > "$OUT/fetch.log" 2>&1
git checkout --detach $COMMIT > "$OUT/checkout.log" 2>&1 || refuse "checkout of $COMMIT failed (checkout.log)"
say "worktree D:\\choptuik-formsq at $(git rev-parse HEAD) (hp/src unchanged since the build's ab2446b8)"
cd "$WT/hp" || exit 1
CMD=("$PY" -u form_s_lastnode.py solvestate $WOUT --state $WOUT/guess_D8000.0000.npz --threads 16 --ladder dd,qd --it_max 2 --it_hi 2 --chord 1 --step_est 3000,600 --delta_tol 1e-15 --tc 1.64519021245138076:1.66e-9 --commit $COMMIT)
{ echo "# $(date -u '+%F %T') UTC cwd $WT/hp OPENBLAS_NUM_THREADS=2 BelowNormal cap $CAP s: ${CMD[*]}"; } > "$OUT/lastnode.log"
s0=$(date +%s)
crun L8000 0 $CAP form_s_lastnode.py "${CMD[@]}" >> "$OUT/lastnode.log" 2>&1
rc=$RC; echo "exit $rc" >> "$OUT/lastnode.log"
say "L8000 solvestate exit $rc, wall $(( $(date +%s) - s0 )) s, capped $CAPPED"
touch "$OUT/L8000.done"
exit 0
