#!/bin/bash
# #954 on dh610: the two builds, one after the other, each in a fresh worktree with a fresh venv (uv, Python 3.14), at nice 10 with CARGO_BUILD_JOBS=8.
# A = origin/main 4c3bb0ef; B = perf/dup-eval 7583e787 with hp/Cargo.toml patched to multidouble's perf/od-dd-const-products (PR #72). multidouble's Python
# package is uninstalled before hp/build.sh. Wall times and the scope's memory.peak in build.log.
. "$(dirname "$0")/common954.sh"
export CARGO_BUILD_JOBS=8
L=$OUT/build.log
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "# $(stamp) UTC $*" >> "$L"; }
peak() { echo "$(( $(cat "$CG/memory.peak") / 1048576 )) MiB"; }
mkdir -p "$R" && git -C "$RAW" fetch -q origin || { log "raw fetch failed"; exit 1; }
for p in $ST $PRED $ST2 T81/ref_main.json T81/scaled_main.json anm-mac/jets_inputs/jets_inputs.json; do
  mkdir -p "$R/$(dirname $p)"; git -C "$RAW" show "origin/main:$p" > "$R/$p" || { log "extract $p failed"; exit 1; }
done
log "inputs extracted into $R"
git -C "$SRC" fetch -q origin main perf/dup-eval || { log "fetch failed"; exit 1; }
build() {
  local name=$1 commit=$2 patch=$3 WT=/home/nathan/Source/choptuik-large-d-954$(echo $1 | tr A-Z a-z)
  [ -d "$WT" ] || git -C "$SRC" worktree add -q --detach "$WT" $commit >> "$L" 2>&1 || { log "$name worktree failed"; return 1; }
  git -C "$WT" checkout -q --detach $commit >> "$L" 2>&1 || { log "$name checkout failed"; return 1; }
  if [ -n "$patch" ] && ! grep -q 'perf/od-dd-const-products' "$WT/hp/Cargo.toml"; then
    printf '\n[patch.crates-io]\nmultidouble = { git = "https://github.com/nmoinvaz/multidouble", branch = "perf/od-dd-const-products" }\n' >> "$WT/hp/Cargo.toml"
  fi
  cd "$WT" || return 1
  log "$name worktree $(git rev-parse HEAD), hp/Cargo.toml patched: $(grep -c 'perf/od-dd-const-products' hp/Cargo.toml)"
  if [ ! -x .venv/bin/python ]; then
    { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 || { log "$name venv failed"; return 1; }
  fi
  . .venv/bin/activate
  uv pip uninstall --python .venv/bin/python multidouble >> "$L" 2>&1 || true
  log "$name $(rustc --version); $(maturin --version); $(python --version)"
  local S=$(date +%s)
  nice -n 10 hp/build.sh >> "$L" 2>&1
  local RC=$?
  log "$name hp/build.sh exit $RC, $(( $(date +%s) - S )) s, peak $(peak)"
  python -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.__file__); print("multidouble", multidouble.__file__)' >> "$L" 2>&1
  deactivate
  return $RC
}
build A 4c3bb0ef "" || { echo "exit 1" >> "$L"; exit 1; }
build B 7583e787 patch || { echo "exit 1" >> "$L"; exit 1; }
echo "exit 0" >> "$L"
