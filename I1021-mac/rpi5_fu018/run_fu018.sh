#!/bin/bash
# #1013 recount4 (rpi5): recount3's 13 unresolved cells (xi1 0.18, argcount 6da7da7b). Each pass values again, from other
# starts and seeds, the points without value in the unresolved leaves (fu_value018.py: dh610's fu_value.py at 0.18). It
# appends each point's first accepted row to the cache, then recounts the 13 cells with recount3's arguments. At most 3
# passes. A pass that accepts no point, or a count with 0 unresolved cells, ends the run. Criteria in README.md.
#   run_fu018.sh CODE PY RAW    CODE: a worktree at 6da7da7b; PY: python; RAW: the raw clone's root.
# Reads I1013-rpi5-cap/recount3 and I1021-mac/rpi5_fu018; writes I1013-rpi5-cap/recount4 (must not exist).
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
CODE=$1; PY=$2; RAW=$3
D=$RAW/I1021-mac/rpi5_fu018; IN=$RAW/I1013-rpi5-cap/recount3; OUT=$RAW/I1013-rpi5-cap/recount4
IS=$CODE/solver/inner_stokes
sha() { if command -v sha256sum > /dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
[ "$(git -C "$CODE" rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C "$CODE" status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e "$OUT" ] && { echo "$OUT exists"; exit 1; }
(cd "$IN" && sha -c --quiet "$D/in/SHA256SUMS_recount3") || { echo "recount3's inputs differ from in/SHA256SUMS_recount3"; exit 1; }
(cd "$D" && sha -c --quiet SHA256SUMS) || { echo "fu_value.py or fu_value018.py differ from SHA256SUMS"; exit 1; }
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
$PY "$D/fu_value018.py" "$CODE" --selftest > "$OUT/logs/fu_selftest.log" 2>&1; a=$?
$PY "$D/fu_value018.py" "$CODE" --selftest --break >> "$OUT/logs/fu_selftest.log" 2>&1; b=$?
echo "fu_value018 selftest, --break exits: $a $b" >> "$X"
[ "$a $b" = "0 1" ] || exit 1
cp -p "$IN/m3/points_M3_r0.18.jsonl" "$IN/m3/points_M3_r0.17.jsonl" "$OUT/m3/"
C=$OUT/m3/points_M3_r0.18.jsonl; SEED=$OUT/m3/points_M3_r0.17.jsonl; CELLS=$IN/m3/leaves_M3_upper_r0.17.jsonl
L=$IN/m3/leaves_M3_recount3_r0.18.jsonl
B="--m3fix --m3starts=0.2,0.25 --m3maxrhs=1e7 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
for n in 1 2 3; do
  R=$OUT/rows_pass$n.jsonl
  echo "pass $n value start $(date -u '+%F %T') leaves $(basename "$L") cache $(wc -l < "$C") lines" >> "$X"
  nice -n 10 timeout 10h $PY -u "$D/fu_value018.py" "$CODE" "$C" "$R" --auto "$L" --procs 4 --append \
    > "$OUT/logs/value_pass$n.log" 2>&1; v=$?
  echo "pass $n value exit $v (0 all accepted, 2 some not) $(date -u '+%F %T'): $(grep '^accepted' "$OUT/logs/value_pass$n.log")" >> "$X"
  for m in f3 lowguard; do
    $PY "$D/fu_value018.py" "$CODE" "$C" "$OUT/retest_${m}_pass$n.jsonl" --retest "$R" --mutate $m > "$OUT/logs/retest_${m}_pass$n.log" 2>&1
    echo "pass $n retest --mutate=$m exit $? (1 fired, 0 changed no decision)" >> "$X"
  done
  [ $v = 0 ] || [ $v = 2 ] || { echo "pass $n value step failed: end" >> "$X"; break; }
  grep -q '^accepted 0 of' "$OUT/logs/value_pass$n.log" && { echo "pass $n accepted no point: end" >> "$X"; break; }
  (cd "$IS" && nice -n 10 timeout 16h $PY -u argcount.py --M=3 --recount="$CELLS" --r1=0.18 --r1b=0.17 --seed="$SEED" $B \
    --out="$OUT/m3" --tag=M3_recount4_pass${n}_r0.18 > "$OUT/logs/recount_pass$n.log" 2>&1); s=$?
  echo "pass $n recount exit $s $(date -u '+%F %T')" >> "$X"
  [ $s = 0 ] || break
  K=$OUT/m3/count_M3_recount4_pass${n}_r0.18.json; L=$OUT/m3/leaves_M3_recount4_pass${n}_r0.18.jsonl
  u=$($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K")
  echo "pass $n unresolved cells $u" >> "$X"
  [ "$u" = 0 ] && break
done
(cd "$IS" && $PY argcount_samebits.py "$IN/m3/points_M3_r0.18.jsonl" "$C") > "$OUT/logs/samebits.log" 2>&1
echo "samebits recount3 -> recount4 exit $? (0)" >> "$X"
echo "end $(date -u '+%F %T')" >> "$X"
exit
}
