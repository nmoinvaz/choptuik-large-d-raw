#!/bin/bash
# #1021 fu021 (rpi5): the recount of record's 11 unresolved cells (xi1 0.17, argcount 6da7da7b). Each pass values again,
# from other starts, bounds and seeds, the points without value in the unresolved leaves (dh610's fu_value.py, unchanged,
# xi1 0.17), skipping points an earlier pass already ran. It appends each point's first accepted row to the cache, then
# recounts the 11 cells with the record's arguments. At most 2 passes. A pass with no new point, a pass that accepts no
# point, or a count with 0 unresolved cells ends the run. Criteria in README.md.
#   run_fu021.sh CODE PY RAW    CODE: a worktree at 6da7da7b; PY: python; RAW: the raw clone's root.
# Reads I1021-mac/final/record and I1021-mac/rpi5_fu021; writes I1021-rpi5/fu021 (must not exist).
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
CODE=$1; PY=$2; RAW=$3
D=$RAW/I1021-mac/rpi5_fu021; IN=$RAW/I1021-mac/final/record; OUT=$RAW/I1021-rpi5/fu021
IS=$CODE/solver/inner_stokes
sha() { if command -v sha256sum > /dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
[ "$(git -C "$CODE" rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C "$CODE" status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e "$OUT" ] && { echo "$OUT exists"; exit 1; }
(cd "$IN" && sha -c --quiet "$D/in/SHA256SUMS_record") || { echo "the record's inputs differ from in/SHA256SUMS_record"; exit 1; }
(cd "$D" && sha -c --quiet SHA256SUMS) || { echo "the scripts differ from SHA256SUMS"; exit 1; }
mkdir -p "$OUT/m3" "$OUT/logs"
X=$OUT/logs/exits.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ echo "start $(date -u '+%F %T') $(uname -srm)"
  $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$X"
(cd "$IS" && { $PY argcount.py --selftest; s=$?
  for m in nocap starts norecount lowcap seedfix; do $PY argcount.py --selftest --mutate=$m; s="$s $?"; done
  echo "argcount selftest, nocap, starts, norecount, lowcap, seedfix exits: $s"; }) > "$OUT/logs/selftest.log" 2>&1
tail -1 "$OUT/logs/selftest.log" >> "$X"
[ "$(tail -1 "$OUT/logs/selftest.log")" = "argcount selftest, nocap, starts, norecount, lowcap, seedfix exits: 0 1 1 1 1 1" ] || exit 1
$PY "$D/fu_value.py" "$CODE" --selftest > "$OUT/logs/fu_selftest.log" 2>&1; a=$?
$PY "$D/fu_value.py" "$CODE" --selftest --break >> "$OUT/logs/fu_selftest.log" 2>&1; b=$?
$PY "$D/prefix_keys.py" "$IN/points_M3_r0.17.jsonl" "$IN/points_M3_r0.17.jsonl" --mutate=edit > "$OUT/logs/prefix_selftest.log" 2>&1; c=$?
echo "fu_value selftest, --break, prefix_keys --mutate=edit exits: $a $b $c" >> "$X"
[ "$a $b $c" = "0 1 1" ] || exit 1
cp -p "$IN/points_M3_r0.17.jsonl" "$IN/points_M3_r0.2.jsonl" "$OUT/m3/"
C=$OUT/m3/points_M3_r0.17.jsonl; SEED=$OUT/m3/points_M3_r0.2.jsonl; CELLS=$D/in/cells_unresolved11.jsonl
L=$IN/leaves_M3_record_r0.17.jsonl
B="--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
DONE=""
for n in 1 2; do
  R=$OUT/rows_pass$n.jsonl
  PTS=$(cd "$D" && $PY select_points.py "$CODE" "$C" "$L" $DONE 2> "$OUT/logs/select_pass$n.log")
  echo "pass $n select: $(cat "$OUT/logs/select_pass$n.log")" >> "$X"
  [ -n "$PTS" ] || { echo "pass $n has no new point: end" >> "$X"; break; }
  echo "pass $n value start $(date -u '+%F %T') leaves $(basename "$L") cache $(wc -l < "$C") lines" >> "$X"
  nice -n 10 timeout 12h $PY -u "$D/fu_value.py" "$CODE" "$C" "$R" --points "$PTS" --procs 4 --append \
    > "$OUT/logs/value_pass$n.log" 2>&1; v=$?
  echo "pass $n value exit $v (0 all accepted, 2 some not) $(date -u '+%F %T'): $(grep '^accepted' "$OUT/logs/value_pass$n.log")" >> "$X"
  DONE="$DONE $R"
  for m in f3 lowguard; do
    $PY "$D/fu_value.py" "$CODE" "$C" "$OUT/retest_${m}_pass$n.jsonl" --retest "$R" --mutate $m > "$OUT/logs/retest_${m}_pass$n.log" 2>&1
    echo "pass $n retest --mutate=$m exit $? (1 fired, 0 changed no decision)" >> "$X"
  done
  [ $v = 0 ] || [ $v = 2 ] || { echo "pass $n value step failed: end" >> "$X"; break; }
  grep -q '^accepted 0 of' "$OUT/logs/value_pass$n.log" && { echo "pass $n accepted no point: end" >> "$X"; break; }
  (cd "$IS" && nice -n 10 timeout 16h $PY -u argcount.py --M=3 --recount="$CELLS" --r1=0.17 --r1b=0.2 --seed="$SEED" $B \
    --out="$OUT/m3" --tag=M3_fu021_pass${n}_r0.17 > "$OUT/logs/recount_pass$n.log" 2>&1); s=$?
  echo "pass $n recount exit $s $(date -u '+%F %T')" >> "$X"
  [ $s = 0 ] || break
  K=$OUT/m3/count_M3_fu021_pass${n}_r0.17.json; L=$OUT/m3/leaves_M3_fu021_pass${n}_r0.17.jsonl
  u=$($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K")
  echo "pass $n unresolved leaves $u" >> "$X"
  [ "$u" = 0 ] && break
done
$PY "$D/prefix_keys.py" "$IN/points_M3_r0.17.jsonl" "$C" > "$OUT/logs/prefix_keys.log" 2>&1
echo "prefix_keys record -> fu021 exit $? (0)" >> "$X"
(cd "$IS" && $PY argcount_samebits.py "$IN/points_M3_r0.17.jsonl" "$C") > "$OUT/logs/samebits.log" 2>&1
echo "samebits record -> fu021 exit $? (reported only: 1 when a guard-blocked point is lifted)" >> "$X"
echo "end $(date -u '+%F %T')" >> "$X"
exit
}
