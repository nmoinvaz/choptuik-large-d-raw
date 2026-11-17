#!/bin/bash
# #946 on dh370: the horizon response's power at D 250.1676 on #603's state re-converged to about 1e-90 (the 4.8.2 build of the #935
# worktree, its .venv). The flags are #603's (run_603.sh) as #808's polish jobs took them (--steps 0, --qd_it 20, --save_base 1,
# the stored plan kept), with --tol_od 1e-90 so that the polish goes past the chain's own 1e-60.
#   run946.sh polish   --selftest, its --mutate=bar control (must fail), then the polish at 12 threads, nice 10
#   run946.sh spread   step_spread.py on the polished base at rel 1e-77,1e-80,1e-82,1e-85, one process per seed (6 threads
#                      each), then step_spread.py power over both with --quad 1.8,2.2 --lin 0.9,1.1
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I946-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_946.txt
cd "$WT/hp" || exit 1
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "946 $1 $(date -u '+%F %T') $(git -C "$WT" rev-parse --short HEAD)" >> "$L"; }
case $1 in
  polish)
    log "polish start"
    nice -n 10 "$PY" step_spread.py --selftest > "$OUT/selftest.log" 2>&1; ST=$?
    nice -n 10 "$PY" step_spread.py --selftest --mutate=bar > "$OUT/selftest_bar.log" 2>&1; SB=$?
    log "selftest exit $ST, selftest --mutate=bar exit $SB (must be non-zero)"
    [ $ST = 0 ] && [ $SB != 0 ] || { log "selftest check failed, stopping"; exit 1; }
    mkdir -p "$OUT/polish"
    nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u anm_run.py "$R" "$OUT/polish" \
      --state I603-win2/chain/anm_pin3_D250.1676.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 \
      --steps 0 --D_max 400 --threads 12 --corrector od --tol_od 1e-90 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 \
      --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_base 1 > "$OUT/polish.log" 2>&1
    log "polish exit $?" ;;
  spread)
    B=$(ls "$OUT"/polish/base_pin3_D250.1676*.npz 2>/dev/null | head -1)
    [ -f "$B" ] || { log "no polished base in polish/"; exit 1; }
    log "spread start, base ${B##*/}"
    for sd in 1 2; do
      ( nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u step_spread.py "$R" "$B" --rel 1e-77,1e-80,1e-82,1e-85 \
          --seeds $sd --controls 0 --repeat 0 --threads 6 --json "$OUT/seed$sd.json" > "$OUT/seed$sd.log" 2>&1
        log "seed $sd exit $?" ) &
    done
    wait
    nice -n 10 "$PY" step_spread.py power "$OUT/seed1.json" "$OUT/seed2.json" --quad 1.8,2.2 --lin 0.9,1.1 --json "$OUT/power.json" \
      > "$OUT/power.log" 2>&1
    log "power exit $?" ;;
  *) echo "usage: run946.sh polish|spread"; exit 2 ;;
esac
