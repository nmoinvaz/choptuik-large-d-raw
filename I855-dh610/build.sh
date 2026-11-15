#!/bin/bash
# #855 on dh610: the worktree of branch hp/multishoot-3 (7e4cfd03) with its own venv (SETUP.md), the reference files
# from the raw repository's origin/main (fetch only, since live chains write into the clone), then hp/build.sh and
# hp/modecount_build.sh at nice 10, with wall times and the scope's memory.peak. No memory guard.
set -u
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-855
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I855-dh610
REF=/home/nathan/scratch855/refs
L=$OUT/build.log
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH CARGO_BUILD_JOBS=4
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
log() { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC $*" >> "$L"; }
peak() { echo "$(( $(cat "$CG/memory.peak") / 1048576 )) MiB"; }
log "start"
mkdir -p "$REF"
git -C "$RAW" fetch -q origin || { log "fetch failed"; exit 1; }
git -C "$RAW" archive origin/main T81/ref_main.json T81/scaled_main.json anm-mac/jets_inputs \
    I523-mac/c3/bits.json I523-mac/c3/bits_perturb.json I523-mac/c3/api.json I523-mac/c3/api_perturb.json \
    I614-dh370/bits.json I614-dh370/bits_perturb.json I614-dh370/api_nan1.json I614-dh370/api_perturb_nan1.json \
    I614-dh370/base I614-dh370/chain_b614 | tar -x -C "$REF" || { log "reference extraction failed"; exit 1; }
log "references: $(find "$REF" -type f | wc -l) files"
if [ ! -d "$WT" ]; then
  { git -C "$SRC" fetch -q origin hp/multishoot-3 && git -C "$SRC" worktree add -q --detach "$WT" 7e4cfd03; } >> "$L" 2>&1 \
    || { log "worktree failed"; exit 1; }
fi
cd "$WT" || exit 1
log "worktree $(git rev-parse HEAD)"
if [ ! -x .venv/bin/python ]; then
  { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 \
    || { log "venv failed"; exit 1; }
fi
. .venv/bin/activate
log "$(cc --version | head -1); $(rustc --version); $(maturin --version); $(python --version); multidouble before: $(pip list 2>/dev/null | grep -ci '^multidouble ')"
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
