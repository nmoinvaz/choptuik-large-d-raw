#!/bin/bash
# #936 on win2: the octo-double residual and Newton step of one stored state of #903's ks-tied chain (ks_chain
# leg06, D 215, ks 230, eight parts, stored plan), from the chain's own build (venv-i600: multidouble 4.1.0,
# multishoot 1.2.1, hpkernel built from D:\choptuik-i600) and from the 4.8.2 build (venv-md482, #935), compared bit
# for bit by #934's state_dump.py. The Python (hp/) is the new worktree's for both, as in #934: the producing
# worktrees (i600, i603r) have no octo_corrector.truth_system. Exits 0 only when the residual and step bits are
# the same and the control (tangents reversed) differs.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
HP=D:/choptuik-i935/hp
RAW=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I936-win2
OLDPY=C:/Users/nathan/Source/venv-i600/Scripts/python.exe
NEWPY=C:/Users/nathan/Source/venv-md482/Scripts/python.exe
L=$OUT/states.log
cd "$OUT" || exit 1
echo "# $(date -u '+%F %T') UTC, new worktree $(git -C /d/choptuik-i935 rev-parse --short HEAD)" > "$L"
step() { echo "== $1 $(date -u '+%H:%M:%S')" >> "$L"; shift; "$@" >> "$L" 2>&1; }
step "dump, venv-i600 (4.1.0)" "$OLDPY" -u state_dump.py "$HP" "$RAW" "$OUT/states_old" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, venv-md482 (4.8.2)" "$NEWPY" -u state_dump.py "$HP" "$RAW" "$OUT/states_new" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, venv-md482, control" "$NEWPY" -u state_dump.py "$HP" "$RAW" "$OUT/states_ctl" --control || { echo "exit 1" >> "$L"; exit 1; }
step "compare" "$NEWPY" -u state_dump.py --compare "$OUT/states_old" "$OUT/states_new" "$OUT/states_ctl"
CMP=$?
echo "# $(date -u '+%F %T') UTC, compare exit $CMP" >> "$L"
echo "exit $CMP" >> "$L"
exit $CMP
