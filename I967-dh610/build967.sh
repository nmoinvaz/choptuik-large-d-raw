#!/bin/bash
# #967 item 1 on dh610: main's hp build on the low-memory recipe in a fresh worktree with a fresh venv (uv, Python 3.14),
# at nice 10 with CARGO_BUILD_JOBS=8, under /usr/bin/time -v. multidouble's Python package is uninstalled first (SETUP.md).
. "$(dirname "$0")/common967.sh"
export CARGO_BUILD_JOBS=8 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
L=$OUT/build.log
log() { echo "# $(stamp) UTC $*" >> "$L"; }
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
cd "$WT" || exit 1
log "worktree $(git rev-parse HEAD), $(git log -1 --format=%s | cut -c1-72)"
log "load $(cut -d' ' -f1-3 /proc/loadavg), $(free -m | awk '/^Mem:/ {print "used " $3 " MiB, available " $7 " MiB"}')"
if [ ! -x .venv/bin/python ]; then
  { uv venv --seed --python 3.14 .venv && uv pip install --python .venv/bin/python -r requirements.txt; } >> "$L" 2>&1 || { log "venv failed"; echo "exit 1" >> "$L"; exit 1; }
fi
. .venv/bin/activate
uv pip uninstall --python .venv/bin/python multidouble >> "$L" 2>&1 || true
log "$(rustc --version); $(cargo --version); $(maturin --version); $(python --version); uv $(uv --version | cut -d' ' -f2)"
log "env CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS CARGO_PROFILE_RELEASE_LTO=$CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS=$CARGO_PROFILE_RELEASE_CODEGEN_UNITS"
S=$(date +%s)
nice -n 10 /usr/bin/time -v -o "$OUT/build_time.txt" hp/build.sh >> "$L" 2>&1
RC=$?
log "hp/build.sh exit $RC, $(( $(date +%s) - S )) s, scope memory.peak $(( $(cat "$CG/memory.peak") / 1048576 )) MiB"
log "load at end $(cut -d' ' -f1-3 /proc/loadavg)"
python -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.__file__); print("multidouble", multidouble.__file__); print("isa", hpkernel.isa(), multidouble.isa())' >> "$L" 2>&1
for c in multidouble multishoot multisolver; do
  log "Cargo.lock $c $(awk -v c=$c '$0 == "name = \"" c "\"" {getline; print $3; exit}' hp/Cargo.lock | tr -d '"')"
done
log "_hpkernel sha1 $(sha1sum $(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/_hpkernel*.so 2>/dev/null | cut -c1-12)"
log "$(grep -E 'Maximum resident|Elapsed' "$OUT/build_time.txt" | tr -s '\t' ' ' | paste -sd';')"
echo "exit $RC" >> "$L"
exit $RC
