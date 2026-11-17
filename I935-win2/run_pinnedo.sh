#!/bin/bash
# #935 follow-up (b): PinnedO.residual_o and newton_o on I903-win2's ks_chain leg06 D 215 state (as #936), with the
# multidouble Python package of 4.6.0 (a93e0896, copied from venv-md482 before the reinstall) and of 4.8.2 (482c6835,
# venv-md482 after the reinstall), the same kernel (venv-md482's hpkernel, 4.8.2) and the same Python (D:\choptuik-i935\hp,
# d7b59668). The two dumps run at once, 5 threads each, BelowNormal.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
HP=D:/choptuik-i935/hp
RAW=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I935-win2
PY=C:/Users/nathan/Source/venv-md482/Scripts/python.exe
PKG460=C:/Users/nathan/AppData/Local/Temp/claude/e3626a297248d1d0/498cd3bf-418e-43b7-b4d4-f77e42690741/scratchpad/md460pkg
L=$OUT/pinnedo.log
cd "$OUT" || exit 1
echo "# $(date -u '+%F %T') UTC, worktree $(git -C /d/choptuik-i935 rev-parse --short HEAD)" > "$L"
PYTHONPATH=$PKG460 "$PY" -u pinnedo_dump.py "$HP" "$RAW" "$OUT/pinnedo_pkg460" > "$OUT/pinnedo_dump_pkg460.log" 2>&1 &
P1=$!
"$PY" -I -u pinnedo_dump.py "$HP" "$RAW" "$OUT/pinnedo_pkg482" > "$OUT/pinnedo_dump_pkg482.log" 2>&1 &
P2=$!
wait $P1; E1=$?; wait $P2; E2=$?
echo "== dumps: 4.6.0 package exit $E1, 4.8.2 package exit $E2 $(date -u '+%H:%M:%S')" >> "$L"
[ $E1 = 0 ] && [ $E2 = 0 ] || { echo "exit 1" >> "$L"; exit 1; }
"$PY" -u pinnedo_dump.py --compare "$OUT/pinnedo_pkg460" "$OUT/pinnedo_pkg482" "$OUT/pinnedo_pkg482" >> "$L" 2>&1
CMP=$?
echo "# $(date -u '+%F %T') UTC, compare exit $CMP" >> "$L"
echo "exit $CMP" >> "$L"
exit $CMP
