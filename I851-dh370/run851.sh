#!/bin/bash
# #851 on dh370: the horizon response's power in rel at D 245.6366, 250.1676 and 252.6135 (octo-double Newton step, step_spread.py,
# the 4.8.2 build of the #935 worktree, its .venv). Order: --selftest must pass and its --mutate=bar control must fail, then the
# three D at once (3 threads each, nice 10), then `power` on the three outputs. --ref is #840's recorded unperturbed step, where
# one exists (D 252.6135, I840-mac/ss_D252.log); the issue's "--ref at 252.6" is that D, not a value.
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I851-dh370
PY=$WT/.venv/bin/python
cd "$WT/hp" || exit 1
L=$OUT/exits_851.txt
echo "start $(date -u '+%F %T') $(git -C "$WT" rev-parse --short HEAD)" >> "$L"
nice -n 10 "$PY" step_spread.py --selftest > "$OUT/selftest.log" 2>&1; ST=$?
nice -n 10 "$PY" step_spread.py --selftest --mutate=bar > "$OUT/selftest_bar.log" 2>&1; SB=$?
echo "selftest exit $ST, selftest --mutate=bar exit $SB (must be non-zero) $(date -u '+%T')" >> "$L"
[ $ST = 0 ] && [ $SB != 0 ] || { echo "selftest check failed, stopping" >> "$L"; exit 1; }
run() { # D [extra args]
  local D=$1; shift
  echo "== $(date -u '+%F %T') $(git -C "$WT" rev-parse --short HEAD) step_spread.py $R I603-win2/chain/anm_pin3_D$D.npz $*" > "$OUT/D$D.log"
  nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u step_spread.py "$R" "$R/I603-win2/chain/anm_pin3_D$D.npz" \
    --rel 1e-70,1e-75,1e-80 --seeds 1 --controls 0 --repeat 0 "$@" --threads 3 --json "$OUT/D$D.json" >> "$OUT/D$D.log" 2>&1
  echo "D$D exit $? $(date -u '+%T')" >> "$L"
}
run 245.6366 &
run 250.1676 &
run 252.6135 --ref 5.2645963792835124e-82 &
wait
nice -n 10 "$PY" step_spread.py power "$OUT/D245.6366.json" "$OUT/D250.1676.json" "$OUT/D252.6135.json" --quad 1.8,2.2 --lin 0.9,1.1 \
  --json "$OUT/power.json" > "$OUT/power.log" 2>&1
echo "power exit $? $(date -u '+%F %T')" >> "$L"
