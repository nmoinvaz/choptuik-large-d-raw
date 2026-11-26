#!/bin/bash
# I1088-win2/L20000 on win2 (the coordinator's order of 2026-11-26 ~02:55 UTC, #1088): D 20000 held at L = 20, direct solve, from the build worktree D:\choptuik-formsq.
# START ONLY ON THE COORDINATOR'S WORD "A" or "B": usage run_L20000.sh A|B   (DRY=1: pins, gate selftest and the build/selftest state only, no checkout, no run)
#   A: --ks 11416 --step_est 5400,900     B: --ks 26018 --step_est 7200,3000
# Refuses unless the build exited 0 and the form-S selftests read as registered (checks_gate.py). Then checks out 1ccd32ab (Python only since the build's ab2446b8: the diff of
# hp/src, the Cargo files, pyproject.toml and build.sh is checked), and runs form_s_lastnode.py solvestate from hp/ with OPENBLAS_NUM_THREADS=1, BelowNormal (started through
# cim_start.ps1), cap 12 h (43200 s) by the exact root pid (crun).
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
RAW=/d/choptuik-i935-raw; WRAW=D:/choptuik-i935-raw
OUT=$RAW/I1088-win2/L20000; WOUT=$WRAW/I1088-win2/L20000
BUILD=$RAW/I1025-win2/hp_form_s_build
WT=/d/choptuik-formsq
V=/c/Users/nathan/Source/venv-formsq; PY=$V/Scripts/python.exe
CAP=43200
COMMIT=1ccd32ab
VAR=${1:-}
case "$VAR" in
  A) KS=11416; EST=5400,900;;
  B) KS=26018; EST=7200,3000;;
  *) echo "usage: run_L20000.sh A|B (only on the coordinator's word)"; exit 2;;
esac
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-formsq PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a "$OUT/L20000_events.txt"; }
refuse() { say "L20000 $VAR STOP: $*"; echo "$*" > "$OUT/L20000_refused_$VAR.txt"; exit ${2:-2}; }
[ -e "$OUT/L20000.done" ] && { echo "refuse: L20000.done exists (move the earlier run's files into a subfolder first)"; exit 2; }
[ -e "$OUT/lastnode.log" ] && [ "${DRY:-0}" != 1 ] && { echo "refuse: lastnode.log exists (a variant already ran: move its files into a subfolder first)"; exit 2; }
h=$(git hash-object --no-filters "$OUT/guess_D20000.0000.npz"); case "$h" in 1f63b72b*) ;; *) refuse "the guess is blob $h, not 1f63b72b";; esac
h=$(git hash-object --no-filters "$OUT/checks_gate.py"); case "$h" in 72ece674*) ;; *) refuse "checks_gate.py is blob $h, not 72ece674";; esac
"$PY" -I "$OUT/checks_gate.py" --selftest > "$OUT/gate_selftest.txt" 2>&1; g0=$?
"$PY" -I "$OUT/checks_gate.py" --selftest --mutate > "$OUT/gate_selftest_mutate.txt" 2>&1; g1=$?
[ "$g0 $g1" = "0 1" ] || refuse "the gate's selftests did not behave (plain $g0, --mutate $g1; wanted 0 1)"
say "variant $VAR (--ks $KS --step_est $EST): pins ok (guess blob 1f63b72b, gate blob 72ece674, gate selftests 0 1)"
rc=$(grep -E '^end .* exit [0-9]+' "$BUILD/build.times" 2>/dev/null | tail -1 | sed 's/.* exit //')
[ "${rc:-x}" = 0 ] || { [ "${DRY:-0}" = 1 ] && { say "DRY: the build has not exited 0 (exit ${rc:-none})"; exit 0; }; refuse "the hp build has not exited 0 (exit ${rc:-none})"; }
[ -e "$BUILD/checks.done" ] || { [ "${DRY:-0}" = 1 ] && { say "DRY: the selftests have not finished"; exit 0; }; refuse "the form-S selftests have not finished (no checks.done)"; }
"$PY" -I "$OUT/checks_gate.py" "$BUILD" > "$OUT/gate_reading.txt" 2>&1; gr=$?
while read l; do say "gate: $l"; done < "$OUT/gate_reading.txt"
[ $gr = 0 ] || { [ "${DRY:-0}" = 1 ] && { say "DRY: the selftests do not read as registered"; exit 0; }; refuse "the form-S selftests did not read as registered (gate_reading.txt)" 3; }
[ "${DRY:-0}" = 1 ] && { say "DRY: all gates pass; no checkout, no run"; exit 0; }
cd "$WT" || exit 1
git diff --quiet ab2446b8 $COMMIT -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/build.sh || refuse "hp/src or the Cargo files differ between ab2446b8 and $COMMIT: the built hpkernel does not match"
git fetch origin > "$OUT/fetch.log" 2>&1
git checkout --detach $COMMIT > "$OUT/checkout.log" 2>&1 || refuse "checkout of $COMMIT failed (checkout.log)"
say "worktree D:\choptuik-formsq at $(git rev-parse HEAD) (hp/src, Cargo files, pyproject and build.sh unchanged since the build's ab2446b8)"
cd "$WT/hp" || exit 1
CMD=("$PY" -u form_s_lastnode.py solvestate $WOUT --state $WOUT/guess_D20000.0000.npz --ks $KS --threads 16 --ladder dd,qd --it_max 2 --it_hi 2 --chord 1 --step_est $EST --delta_tol 1e-15 --tc 1.64441243858130260:1.77e-9 --commit $COMMIT)
{ echo "# $(date -u '+%F %T') UTC variant $VAR cwd $WT/hp OPENBLAS_NUM_THREADS=1 BelowNormal cap $CAP s: ${CMD[*]}"; } > "$OUT/lastnode.log"
s0=$(date +%s)
crun L20000_$VAR 0 $CAP form_s_lastnode.py "${CMD[@]}" >> "$OUT/lastnode.log" 2>&1
rc=$RC; echo "exit $rc" >> "$OUT/lastnode.log"
say "L20000 $VAR solvestate exit $rc, wall $(( $(date +%s) - s0 )) s, capped $CAPPED"
touch "$OUT/L20000.done"
exit 0
