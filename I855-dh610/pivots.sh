#!/bin/bash
# #855, after checks.sh: the worktree moved to branch hp/clu-pivots (multidouble 4.6.0, whose clu_pivots replaces
# modecount_cx's copied LU), modecount_cx rebuilt (hpkernel is left as build.sh made it: 4.6.0 changes only the complex
# LU, which hpkernel does not call), then modecount_check.py's checks 1, 2, 4 and 6 (with the pivots) and the dmat
# control, nice 10.
set -u
WT=/home/nathan/Source/choptuik-large-d-855
OUT=/home/nathan/Source/choptuik-large-d-raw/I855-dh610
L=$OUT/pivots.log
cd "$WT" || exit 1
git fetch -q origin hp/clu-pivots && git checkout -q --detach FETCH_HEAD || { echo "checkout failed" > "$L"; exit 1; }
. .venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC worktree $(git rev-parse HEAD)" > "$L"
( cd hp/modecount_cx && cargo fetch --locked -q ) >> "$L" 2>&1
S=$(date +%s); nice -n 10 hp/modecount_build.sh >> "$L" 2>&1; RC=$?
echo "# modecount_build.sh exit $RC, $(( $(date +%s) - S )) s" >> "$L"
[ $RC -eq 0 ] || { echo "exit $RC" >> "$L"; exit $RC; }
cd hp
nice -n 10 python modecount_check.py data/states/up2_D20.0437.npz --quick --out="$OUT/modecount_check_pivots.jsonl" >> "$L" 2>&1
RC1=$?
echo "# modecount_check exit $RC1 (0 = pass)" >> "$L"
nice -n 10 python modecount_check.py data/states/up2_D20.0437.npz --quick --mutate=dmat --out="$OUT/modecount_check_pivots.jsonl" >> "$L" 2>&1
RC2=$?
echo "# modecount_check --mutate=dmat exit $RC2 (1 = the control fires)" >> "$L"
[ $RC1 -eq 0 ] && [ $RC2 -eq 1 ]; echo "exit $?" >> "$L"
