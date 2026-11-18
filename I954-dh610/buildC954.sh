#!/bin/bash
# #954 (the coordinator's addition): build C = PR #955's branch perf/series-par-at (the series' order-k sums split over threads; its hp/Cargo.toml already patches multidouble to PR #77's
# branch perf/field-par-at-sums), a fresh worktree and venv, nice 10, CARGO_BUILD_JOBS=8, after the builds of A and B. Wall time and peak in buildC.log.
. "$(dirname "$0")/common954.sh"
export CARGO_BUILD_JOBS=8
L=$OUT/buildC.log
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "# $(stamp) UTC $*" >> "$L"; }
peak() { echo "$(( $(cat "$CG/memory.peak") / 1048576 )) MiB"; }
WT=/home/nathan/Source/choptuik-large-d-954c
git -C "$SRC" fetch -q origin perf/series-par-at || { log "fetch failed"; echo "exit 1" >> "$L"; exit 1; }
C=$(git -C "$SRC" rev-parse origin/perf/series-par-at)
[ -d "$WT" ] || git -C "$SRC" worktree add -q --detach "$WT" $C >> "$L" 2>&1 || { log "worktree failed"; echo "exit 1" >> "$L"; exit 1; }
git -C "$WT" checkout -q --detach $C >> "$L" 2>&1
cd "$WT" || exit 1
log "C worktree $(git rev-parse HEAD), patch lines in hp/Cargo.toml: $(grep -c 'perf/field-par-at-sums' hp/Cargo.toml)"
if [ ! -x .venv/bin/python ]; then
  { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 || { log "venv failed"; echo "exit 1" >> "$L"; exit 1; }
fi
. .venv/bin/activate
uv pip uninstall --python .venv/bin/python multidouble >> "$L" 2>&1 || true
log "C $(rustc --version); $(maturin --version); $(python --version)"
S=$(date +%s)
nice -n 10 hp/build.sh >> "$L" 2>&1
RC=$?
log "C hp/build.sh exit $RC, $(( $(date +%s) - S )) s, peak $(peak)"
python -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.__file__); print("multidouble", multidouble.__file__)' >> "$L" 2>&1
echo "exit $RC" >> "$L"
exit $RC
