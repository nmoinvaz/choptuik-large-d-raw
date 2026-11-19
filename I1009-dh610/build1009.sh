#!/bin/bash
# #1009 step 3: hp/build.sh in the new worktree with the new venv, low-memory recipe, 6 jobs, nice 10 (run as the user unit i1009-build, MemoryMax 30G).
. "$(dirname "$0")/common1009.sh"
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6
L=$OUT/build.log
log() { echo "# $(stamp) UTC $*" >> "$L"; }
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
cd "$WT" || exit 1
log "worktree $(git rev-parse HEAD), $(git log -1 --format=%s | cut -c1-72)"
log "load $(cut -d' ' -f1-3 /proc/loadavg), $(free -m | awk '/^Mem:/ {print "used " $3 " MiB, available " $7 " MiB"}')"
. $VENV/bin/activate
log "$(rustc --version); $(cargo --version); $(maturin --version); $(python --version); VIRTUAL_ENV=$VIRTUAL_ENV"
S=$(date +%s)
nice -n 10 /usr/bin/time -v -o "$OUT/build_time.txt" hp/build.sh >> "$L" 2>&1
RC=$?
log "hp/build.sh exit $RC, $(( $(date +%s) - S )) s, unit memory.peak $(( $(cat "$CG/memory.peak" 2>/dev/null || echo 0) / 1048576 )) MiB"
python -c 'import hpkernel, multidouble; print("hpkernel", hpkernel.__file__); print("multidouble", multidouble.__file__); print("isa", hpkernel.isa(), multidouble.isa())' >> "$L" 2>&1
for c in multidouble multishoot multisolver; do
  log "Cargo.lock $c $(awk -v c=$c '$0 == "name = \"" c "\"" {getline; print $3; getline; print $3; exit}' hp/Cargo.lock | tr -d '"' | tr '\n' ' ')"
done
grep -A3 'name = "multidouble"' hp/Cargo.lock | head -4 >> "$L"
log "$(grep -E 'Maximum resident|Elapsed' "$OUT/build_time.txt" | tr -s '\t' ' ' | paste -sd';')"
echo "exit $RC" >> "$L"
exit $RC
