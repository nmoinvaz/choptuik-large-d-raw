#!/bin/bash
# #858 on dh610, after #855: octo_corrector.py wall from #608 restart4_d6's prediction at D 253.3382 with the chain's
# corrector options, the LU in octo-double (--lu od, as the chain) and in quad-double (--lu qd), concurrently at 6
# threads each (the same load), nice 10; then the control --lu qd --mutate 10; then compare.py on the results.
set -u
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-858
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I858-dh610
PRED=I608-dh610/restart4_d6/pred_pin3_D253.3382.npz
ACC=$RAW/I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
if [ ! -d "$WT" ]; then
  { git -C "$SRC" fetch -q origin hp/mixed-corrector && git -C "$SRC" worktree add -q --detach "$WT" cf7bd594; } || exit 1
fi
cd "$WT/hp" && . /home/nathan/Source/choptuik-large-d-855/.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
OPTS="--threads 6 --tol 1e-60 --F_max 1e-58 --it_max 12 --accept natural --strong 4 --full_drop 1e-2 --reseed_o 3 --held_o 1 --reseed_start pred"
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg): $*" > "$OUT/$name.log"
  local t=$(date +%s)
  nice -n 10 python -u octo_corrector.py wall $RAW $PRED $OPTS "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $? wall $(( $(date +%s) - t )) s" >> "$OUT/$name.log"
}
run wall_od --lu od --out "$OUT/wall_od" &
run wall_qd --lu qd --out "$OUT/wall_qd" &
wait
run wall_qd_mutate10 --lu qd --mutate 10
C="python $OUT/compare.py $WT/hp"
{ echo "== 3. qd against od"; $C "$OUT/wall_od.npz" "$OUT/wall_qd.npz" 1e-50; echo "exit $?"
  echo "== 4. control: od against the prediction (must differ)"; $C "$OUT/wall_od.npz" "$RAW/$PRED" 1e-50; echo "exit $?"
  echo "== 6. od against the chain's accepted state"; $C "$OUT/wall_od.npz" "$ACC" 1e-50; echo "exit $?"
  echo "== 6. qd against the chain's accepted state"; $C "$OUT/wall_qd.npz" "$ACC" 1e-50; echo "exit $?"; } > "$OUT/compare.log" 2>&1
echo "done $(date -u '+%H:%M')" > "$OUT/done.txt"
