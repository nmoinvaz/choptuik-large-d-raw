#!/bin/bash
# #946 addendum on dh370 (the coordinator's order): seed 2 at D 245.6366 and D 252.6135 at #851's rels (1e-70, 1e-75, 1e-80), the
# two D side by side (6 threads each, nice 10), then step_spread.py power over both. --ref only at D 252.6135, #840's recorded step.
# Same worktree and build as #851 and #946 (the 935 worktree, its .venv).
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I946-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_946.txt
cd "$WT/hp" || exit 1
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "946 $1 $(date -u '+%F %T') $(git -C "$WT" rev-parse --short HEAD)" >> "$L"; }
log "seed 2 start"
run() { # D [extra args]
  local D=$1; shift
  nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u step_spread.py "$R" "$R/I603-win2/chain/anm_pin3_D$D.npz" \
    --rel 1e-70,1e-75,1e-80 --seeds 2 --controls 0 --repeat 0 "$@" --threads 6 --json "$OUT/D${D}_seed2.json" > "$OUT/D${D}_seed2.log" 2>&1
  log "D$D seed 2 exit $?"
}
run 245.6366 &
run 252.6135 --ref 5.2645963792835124e-82 &
wait
nice -n 10 "$PY" step_spread.py power "$OUT/D245.6366_seed2.json" "$OUT/D252.6135_seed2.json" --quad 1.8,2.2 --lin 0.9,1.1 \
  --json "$OUT/power_seed2.json" > "$OUT/power_seed2.log" 2>&1
log "seed 2 power exit $?"
