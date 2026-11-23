#!/bin/bash
# #1076 fu022mp: fu021's guard-blocked points valued with the M = 3 inner solve in mpmath (value_mp.py batch), then
# the recount of the record's 11 cells with the record's arguments; at most 2 passes, as run_fu021.sh. A pass with no
# new point, a pass that values no point, or a count with 0 unresolved leaves ends the run. Criteria in README.md.
#   run_fu022mp.sh CODE PY RAW PROCS    CODE: a worktree at the commit in README.md; PY: python with numpy, scipy,
#                                       mpmath; RAW: the raw clone's root; PROCS: processes for the valuing
# Reads I1021-rpi5/fu021 and I1021-mac/rpi5_fu021; writes I1021-<host>/fu022mp (OUT, must not exist).
set -u
{ # read whole before it runs
CODE=$1; PY=$2; RAW=$3; PROCS=$4
COMMIT=$(cat "$RAW/I1021-mac/fu022mp/CODE_COMMIT")
D=$RAW/I1021-mac/fu022mp; F21=$RAW/I1021-rpi5/fu021/m3; S21=$RAW/I1021-mac/rpi5_fu021
OUT=$RAW/I1021-$(hostname -s | tr 'A-Z' 'a-z' | cut -c1-12)/fu022mp
IS=$CODE/solver/inner_stokes
sha() { if command -v sha256sum > /dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
[ "$(git -C "$CODE" rev-parse HEAD)" = "$COMMIT" ] || { echo "CODE is not at $COMMIT"; exit 1; }
[ -z "$(git -C "$CODE" status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e "$OUT" ] && { echo "$OUT exists"; exit 1; }
(cd "$F21" && sha -c --quiet "$D/SHA256SUMS_fu021") || { echo "fu021's inputs differ from SHA256SUMS_fu021"; exit 1; }
mkdir -p "$OUT/m3" "$OUT/logs"
X=$OUT/logs/exits.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ echo "start $(date -u '+%F %T') $(uname -srm) commit $COMMIT"
  $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$X"
cp -p "$F21/points_M3_r0.17.jsonl" "$F21/points_M3_r0.2.jsonl" "$OUT/m3/"
C=$OUT/m3/points_M3_r0.17.jsonl; SEED=$OUT/m3/points_M3_r0.2.jsonl; CELLS=$S21/in/cells_unresolved11.jsonl
L=$F21/leaves_M3_fu021_pass2_r0.17.jsonl
(cd "$IS" && nice -n 10 $PY -u value_mp.py check1 "$C" --n=1 > "$OUT/logs/check1.log" 2>&1; a=$?
 nice -n 10 $PY -u value_mp.py check1 "$C" --n=1 --mutate=conv > "$OUT/logs/check1_conv.log" 2>&1; b=$?
 echo "value_mp check1, check1 --mutate=conv exits: $a $b" >> "$X")
[ "$(tail -1 "$X")" = "value_mp check1, check1 --mutate=conv exits: 0 1" ] || { echo "preflight failed" >> "$X"; exit 1; }
B="--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
DONE=""
for n in 1 2; do
  R=$OUT/rows_pass$n.jsonl
  PTS=$(cd "$S21" && $PY select_points.py "$CODE" "$C" "$L" $DONE 2> "$OUT/logs/select_pass$n.log")
  echo "pass $n select: $(cat "$OUT/logs/select_pass$n.log")" >> "$X"
  [ -n "$PTS" ] || { echo "pass $n has no new point: end" >> "$X"; break; }
  echo "pass $n value start $(date -u '+%F %T') cache $(wc -l < "$C") lines" >> "$X"
  (cd "$IS" && nice -n 10 $PY -u value_mp.py batch "$C" "$R" --points "$PTS" --procs="$PROCS" > "$OUT/logs/value_pass$n.log" 2>&1); v=$?
  echo "pass $n value exit $v $(date -u '+%F %T'): $(tail -1 "$OUT/logs/value_pass$n.log")" >> "$X"
  DONE="$DONE $R"
  [ $v = 0 ] || { echo "pass $n value step failed: end" >> "$X"; break; }
  grep -q '^valued 0 of' "$OUT/logs/value_pass$n.log" && { echo "pass $n valued no point: end" >> "$X"; break; }
  (cd "$IS" && nice -n 10 timeout 16h $PY -u argcount.py --M=3 --recount="$CELLS" --r1=0.17 --r1b=0.2 --seed="$SEED" $B \
    --out="$OUT/m3" --tag=M3_fu022mp_pass${n}_r0.17 > "$OUT/logs/recount_pass$n.log" 2>&1); s=$?
  echo "pass $n recount exit $s $(date -u '+%F %T')" >> "$X"
  [ $s = 0 ] || break
  K=$OUT/m3/count_M3_fu022mp_pass${n}_r0.17.json; L=$OUT/m3/leaves_M3_fu022mp_pass${n}_r0.17.jsonl
  u=$($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K")
  echo "pass $n unresolved leaves $u" >> "$X"
  [ "$u" = 0 ] && break
done
$PY "$S21/prefix_keys.py" "$F21/points_M3_r0.17.jsonl" "$C" > "$OUT/logs/prefix_keys.log" 2>&1
echo "prefix_keys fu021 -> fu022mp exit $? (0)" >> "$X"
echo "end $(date -u '+%F %T')" >> "$X"
exit
}
