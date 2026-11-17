#!/bin/bash
# #934: the octo-double residual and Newton step on two stored chain states (#903's chain_k160 at D 231, #841's chain
# at D 259.5166), with the 4.8.0 build (#923's worktree and venv) and the new build, compared bit for bit (state_dump.py),
# then octo_corrector.py planted on the D 231 state with the new build and its control. 5 CPUs, nice 10. Exits 0 only
# when the residuals and steps are the same bits, the step control differs, planted passes and its control fails.
taskset -cp 0-4 $$ > /dev/null  # 5 of the 20 CPUs: two chains use the rest
NEW=/home/nathan/Source/choptuik-large-d-934
OLD=/home/nathan/Source/choptuik-large-d-923
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
ST=/home/nathan/scratch934/states
L=$OUT/states.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
git -C "$RAW" fetch -q origin || { echo "fetch failed" > "$L"; exit 1; }
for p in I903-dh610/chain_k160/anm_pin3_D231.0000.npz I841-dh370/chain/anm_pin3_D259.5166.npz; do
  mkdir -p "$ST/$(dirname "$p")"
  git -C "$RAW" show "origin/main:$p" > "$ST/$p" || { echo "extract $p failed" > "$L"; exit 1; }
done
echo "# $(date -u '+%F %T') UTC, new $(git -C "$NEW" rev-parse --short HEAD), old $(git -C "$OLD" rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L"
cd "$OUT" || exit 1
step() { echo "== $1 $(date -u '+%H:%M:%S')" >> "$L"; shift; nice -n 10 "$@" >> "$L" 2>&1; }
step "dump, 4.8.0" "$OLD/.venv/bin/python" -u state_dump.py "$NEW/hp" "$ST" "$OUT/states_old" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, new" "$NEW/.venv/bin/python" -u state_dump.py "$NEW/hp" "$ST" "$OUT/states_new" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, new, control" "$NEW/.venv/bin/python" -u state_dump.py "$NEW/hp" "$ST" "$OUT/states_ctl" --control || { echo "exit 1" >> "$L"; exit 1; }
step "compare" "$NEW/.venv/bin/python" -u state_dump.py --compare "$OUT/states_old" "$OUT/states_new" "$OUT/states_ctl"
CMP=$?
cd "$NEW/hp" || exit 1
step "planted" "$NEW/.venv/bin/python" -u octo_corrector.py planted "$ST" I903-dh610/chain_k160/anm_pin3_D231.0000.npz --threads 5
PL=$?
step "planted, control --mutate 10" "$NEW/.venv/bin/python" -u octo_corrector.py planted "$ST" I903-dh610/chain_k160/anm_pin3_D231.0000.npz --threads 5 --qd 0 --mutate 10
PC=$?
echo "# $(date -u '+%F %T') UTC, compare exit $CMP, planted exit $PL, planted control exit $PC, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$L"
RC=0; [ $CMP = 0 ] && [ $PL = 0 ] && [ $PC != 0 ] || RC=1
echo "exit $RC" >> "$L"
exit $RC
