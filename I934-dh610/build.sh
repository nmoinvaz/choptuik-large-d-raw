#!/bin/bash
# #934 on dh610 the worktree of branch hp/multidouble-4.8.2 at cdb5a6bc with its own venv (SETUP.md), the references
# from the raw repository's origin/main (fetch only), then hp/build.sh and hp/modecount_build.sh at nice 10, with wall
# times and the scope's memory.peak. No memory guard.
taskset -cp 0-4 $$ > /dev/null  # 5 of the 20 CPUs: two chains use the rest
set -u
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-934
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
REF=/home/nathan/scratch934/refs
L=$OUT/build.log
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH CARGO_BUILD_JOBS=5
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $*" >> "$L"; }
peak() { echo "$(( $(cat "$CG/memory.peak") / 1048576 )) MiB"; }
log "start"
mkdir -p "$REF"
git -C "$RAW" fetch -q origin || { log "fetch failed"; exit 1; }
git -C "$RAW" archive origin/main T81/ref_main.json T81/scaled_main.json anm-mac/jets_inputs \
    I855-dh610/bits.json I855-dh610/bits_perturb.json I855-dh610/api.json I855-dh610/api_perturb.json \
    | tar -x -C "$REF" || { log "reference extraction failed"; exit 1; }
log "references: $(find "$REF" -type f | wc -l) files"
git -C "$SRC" fetch -q origin hp/multidouble-4.8.2 >> "$L" 2>&1 || { log "fetch failed"; exit 1; }
if [ ! -d "$WT" ]; then
  git -C "$SRC" worktree add -q --detach "$WT" cdb5a6bc >> "$L" 2>&1 || { log "worktree failed"; exit 1; }
fi
git -C "$WT" checkout -q --detach cdb5a6bc >> "$L" 2>&1 || { log "checkout failed"; exit 1; }
cd "$WT" || exit 1
log "worktree $(git rev-parse HEAD)"
if [ ! -x .venv/bin/python ]; then
  { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 \
    || { log "venv failed"; exit 1; }
fi
. .venv/bin/activate
log "$(cc --version | head -1); $(rustc --version); $(maturin --version); $(python --version)"
S=$(date +%s)
nice -n 10 hp/build.sh >> "$L" 2>&1
RC=$?
log "hp/build.sh exit $RC, $(( $(date +%s) - S )) s, peak $(peak)"
[ $RC -eq 0 ] || { echo "exit $RC" >> "$L"; exit $RC; }
S=$(date +%s)
nice -n 10 hp/modecount_build.sh >> "$L" 2>&1
RC=$?
log "hp/modecount_build.sh exit $RC, $(( $(date +%s) - S )) s, peak $(peak)"
python -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.__file__); print("multidouble", multidouble.__file__)' >> "$L" 2>&1
echo "exit $RC" >> "$L"
exit $RC
