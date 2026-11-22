#!/bin/bash
# #1025 (coordinator hc 2026-11-22 ~03:00 UTC): xfkappa's k_c 63 leap states from D 18.5 to D 20, winb's flags, h 0.0625, 6 threads, nice 10, 12 h cap; mirrors the worktree's data/ files of the tag into raw.
{
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
SRC=/home/nathan/Source/choptuik-large-d-raw-push960/I1025-mac/d18          # xfkappa's states, read only (raw origin/main)
OUT=$RAW/I1025-dh370/kc63_leap
WT=/home/nathan/Source/choptuik-large-d-1025
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc63dh370
SUM=$OUT/summary_leap.txt
mkdir -p $OUT
stamp() { date -u '+%F %T'; }
log() { echo "1025 leap $* $(stamp) UTC" >> $OUT/exits_leap.txt; }
echo "# k_c 63 leap on dh370: started $(stamp) UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" > $SUM
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { log "worktree not at 48c36355: stop"; exit 1; }
[ -z "$(git -C $WT status --short solver | head -1)" ] || { log "worktree solver/ has changes: stop"; exit 1; }
[ "$(git -C $WT hash-object $WT/solver/matter/ell_leap.py | cut -c1-8)" = 1eb873e4 ] || { log "ell_leap.py is not xfkappa's pin 1eb873e4: stop"; exit 1; }
echo "code: worktree 48c36355, ell_leap.py blob 1eb873e4 (xfkappa's pin), $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa(), hasattr(m,"dd_logdet"))')" >> $SUM
$PY - >> $SUM 2>&1 <<PYEOF
import json, numpy as np
src = "$SRC"
recs = {r["D"]: r for r in map(json.loads, open(src + "/l1kc63Wm1025.jsonl"))}
for D, f in ((18.4375, "sol_l1kc63Wm1025_D18.437500.npy"), (18.5, "sol_l1kc63Wm1025_D18.500000.npy")):
    z = np.load(src + "/" + f)
    ok = abs(z[-1] - recs[D]["Delta"]) <= 1e-15
    print(f"input {f}: shape {z.shape}, z[-1] {z[-1]!r}, record Delta {recs[D]['Delta']!r}, {'equal' if ok else 'DIFFERENT'}; record |F| {recs[D]['F']:.3e}, constraint {recs[D]['constraint']:.3e}, steps {recs[D]['steps']}")
    assert ok
PYEOF
[ $? = 0 ] || { log "an input state differs from its record: stop"; exit 1; }
cd $WT/solver/matter || exit 9
CMD="nice -n 10 timeout 43200 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_leap.py $TAG 1 63 $SRC/sol_l1kc63Wm1025_D18.437500.npy 18.4375 $SRC/sol_l1kc63Wm1025_D18.500000.npy 18.5 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
echo "== $(stamp) -u ell_leap.py $TAG 1 63 sol_l1kc63Wm1025_D18.437500.npy 18.4375 sol_l1kc63Wm1025_D18.500000.npy 18.5 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold (6 threads, nice 10, timeout 43200 s)" > $OUT/leap.log
echo "cmd: $CMD" >> $SUM
log "starting the leap (6 threads, nice 10, cap 43200 s), load $(cut -d' ' -f1-3 /proc/loadavg)"
t0=$(date +%s)
$CMD >> $OUT/leap.log 2>&1 &
pid=$!
log "leap pid $pid"
while kill -0 $pid 2>/dev/null; do
  sleep 300
  cp -u data/*${TAG}* $OUT/ 2>/dev/null
done
wait $pid; rc=$?
cp -u data/*${TAG}* $OUT/ 2>/dev/null
echo "leap exit $rc, wall $(( $(date +%s) - t0 )) s; last lines: $(tail -2 $OUT/leap.log | cut -c1-200 | tr '\n' '|')" >> $SUM
log "leap exit $rc wall $(( $(date +%s) - t0 )) s"
exit 0
}
