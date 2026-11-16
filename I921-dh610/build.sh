#!/bin/bash
# #921 on dh610: the worktree of branch hp/jac-tangents (c1f07296) with its own venv (SETUP.md), then hp/build.sh at nice
# 10, with its wall time and the scope's memory.peak. No memory guard.
set -u
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-921
OUT=/home/nathan/Source/choptuik-large-d-raw/I921-dh610
L=$OUT/build.log
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH CARGO_BUILD_JOBS=4
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $*" >> "$L"; }
peak() { echo "$(( $(cat "$CG/memory.peak") / 1048576 )) MiB"; }
log "start"
if [ ! -d "$WT" ]; then
  { git -C "$SRC" fetch -q origin hp/jac-tangents && git -C "$SRC" worktree add -q --detach "$WT" c1f07296; } >> "$L" 2>&1 \
    || { log "worktree failed"; exit 1; }
fi
cd "$WT" || exit 1
log "worktree $(git rev-parse HEAD)"
if [ ! -x .venv/bin/python ]; then
  { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 \
    || { log "venv failed"; exit 1; }
fi
. .venv/bin/activate
log "$(rustc --version); $(python --version)"
S=$(date +%s)
nice -n 10 hp/build.sh >> "$L" 2>&1
RC=$?
log "hp/build.sh exit $RC, $(( $(date +%s) - S )) s, peak $(peak)"
python -c 'import hpkernel; print("hpkernel", hpkernel.__file__)' >> "$L" 2>&1
echo "exit $RC" >> "$L"
exit $RC
