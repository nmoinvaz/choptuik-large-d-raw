#!/bin/bash
# #935 on win2: the reference checks of the 4.8.2 build (worktree D:\choptuik-i935, venv-md482), from #934's
# checks.sh: ref, scaled, jets and jets --mutate=kappa, three chains in parallel at BelowNormal (started by cmd start),
# 1 BLAS thread each. References from the raw clone beside this folder (the Windows reference for ref).
# Exits non-zero when a check that must pass fails or the kappa control passes.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=C:/Users/nathan/Source/venv-md482/Scripts/python.exe
REF=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I935-win2
cd /d/choptuik-i935/hp || exit 1
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"
  "$PY" -u "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
J=$REF/anm-mac/jets_inputs/jets_inputs.json
chain_ref()    { run ref highm_check.py ref --compare=$REF/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80; }
chain_scaled() { run scaled highm_check.py scaled --compare=$REF/T81/scaled_main.json; }
chain_jets()   { run jets highm_check.py jets --compare=$J
                 run jets_mutate_kappa highm_check.py jets --compare=$J --mutate=kappa; }
echo "# $(date -u '+%F %T') UTC" > "$OUT/checks_done.txt"
chain_ref & chain_scaled & chain_jets & wait
rc=0
for n in ref scaled jets; do [ "$(tail -1 "$OUT/$n.log")" = "exit 0" ] || rc=1; done
[ "$(tail -1 "$OUT/jets_mutate_kappa.log")" != "exit 0" ] || rc=1
echo "# $(date -u '+%F %T') UTC, rc $rc" >> "$OUT/checks_done.txt"
exit $rc
