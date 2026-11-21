#!/bin/bash
# #1013 loc018 (rpi5): the zeros in recount3's two lower unions at xi1 0.18 (argcount 6da7da7b). Stage 1 locates each
# by argcount's Newton from the union's centre, with a planted control box. Stage 2 counts a relocation box under 0.02
# around each located zero, plain and with the plant. Criteria in README.md and locate018.py, fixed before the run.
#   run_loc018.sh CODE PY RAW    CODE: a worktree at 6da7da7b; PY: python; RAW: the raw clone's root.
# Reads I1013-rpi5-cap/recount3 and I1021-mac/rpi5_loc018; writes I1013-rpi5-cap/loc018 (must not exist).
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
CODE=$1; PY=$2; RAW=$3
D=$RAW/I1021-mac/rpi5_loc018; IN=$RAW/I1013-rpi5-cap/recount3; OUT=$RAW/I1013-rpi5-cap/loc018
IS=$CODE/solver/inner_stokes
sha() { if command -v sha256sum > /dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
[ "$(git -C "$CODE" rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C "$CODE" status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e "$OUT" ] && { echo "$OUT exists"; exit 1; }
(cd "$IN" && sha -c --quiet "$D/in/SHA256SUMS_recount3") || { echo "recount3's inputs differ from in/SHA256SUMS_recount3"; exit 1; }
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
$PY "$D/locate018.py" --selftest > "$OUT/logs/locate018_selftest.log" 2>&1; a=$?
$PY "$D/plant_check.py" --selftest > "$OUT/logs/plant_check_selftest.log" 2>&1; b=$?
echo "locate018 selftest, plant_check selftest exits: $a $b" >> "$X"
[ "$a $b" = "0 0" ] || exit 1
cp -p "$IN/m3/points_M3_r0.18.jsonl" "$IN/m3/points_M3_r0.17.jsonl" "$OUT/m3/"
C=$OUT/m3/points_M3_r0.18.jsonl; SEED=$OUT/m3/points_M3_r0.17.jsonl
$PY "$D/union_winding.py" "$CODE" "$C" "$IN/m3/leaves_M3_recount3_r0.18.jsonl" "$IN/m3/count_M3_recount3_r0.18.json" \
  > "$OUT/logs/union_winding.log" 2>&1; a=$?
$PY "$D/union_winding.py" "$CODE" "$C" "$IN/m3/leaves_M3_recount3_r0.18.jsonl" "$IN/m3/count_M3_recount3_r0.18.json" \
  --mutate=conj >> "$OUT/logs/union_winding.log" 2>&1; b=$?
echo "union_winding, --mutate=conj exits: $a $b" >> "$X"
[ "$a $b" = "0 1" ] || exit 1
# stage 1: Newton from the unions' centres and from C0 (planted)
echo "stage 1 start $(date -u '+%F %T')" >> "$X"
(cd "$IS" && nice -n 10 timeout 8h $PY -u "$D/locate018.py" run "$CODE" "$C" "$SEED" "$OUT/locate.json" --procs 4) \
  > "$OUT/logs/locate.log" 2>&1
echo "stage 1 exit $? $(date -u '+%F %T')" >> "$X"
$PY "$D/locate018.py" check "$OUT/locate.json" > "$OUT/logs/check.log" 2>&1; s=$?
for m in shift sign; do $PY "$D/locate018.py" check "$OUT/locate.json" --mutate=$m >> "$OUT/logs/check.log" 2>&1; s="$s $?"; done
echo "stage 1 check, --mutate=shift, --mutate=sign exits: $s (0 both unions or 2 one, then 1 1)" >> "$X"
case "$s" in "0 1 1"|"2 1 1") ;; *) echo "stage 1 does not pass: end" >> "$X"; exit 1;; esac
# stage 2: relocation boxes B1, B2 and the control box C0, recounted plain and with the plant at P0
$PY "$D/locate018.py" boxes "$OUT/locate.json" > "$OUT/leaf_boxes.jsonl"
P0=$($PY -B -c "import sys; sys.path.insert(0, '$D'); import locate018 as L; print(f'{L.P0[0]},{L.P0[1]}')")
B="--M=3 --recount=$OUT/leaf_boxes.jsonl --r1=0.18 --r1b=0.17 --seed=$SEED --m3fix --m3starts=0.2,0.25 --m3maxrhs=1e7"
B="$B --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry --out=$OUT/m3"
for t in plain plant; do
  echo "stage 2 $t start $(date -u '+%F %T')" >> "$X"
  (cd "$IS" && nice -n 10 timeout 8h $PY -u argcount.py $B --tag=M3_loc018_${t}_r0.18 $([ $t = plant ] && echo --plant=$P0)) \
    > "$OUT/logs/recount_$t.log" 2>&1
  echo "stage 2 $t exit $? $(date -u '+%F %T')" >> "$X"
done
KP=$OUT/m3/count_M3_loc018_plain_r0.18.json; KQ=$OUT/m3/count_M3_loc018_plant_r0.18.json
$PY "$D/locate018.py" check2 "$KP" "$OUT/locate.json" > "$OUT/logs/check2.log" 2>&1; s=$?
for m in shift sign; do $PY "$D/locate018.py" check2 "$KP" "$OUT/locate.json" --mutate=$m >> "$OUT/logs/check2.log" 2>&1; s="$s $?"; done
echo "stage 2 check2, --mutate=shift, --mutate=sign exits: $s (0 1 1)" >> "$X"
$PY "$D/plant_check.py" "$KQ" --record "$KP" --at "$P0" > "$OUT/logs/plant_check.log" 2>&1; s=$?
$PY "$D/plant_check.py" "$KQ" --record "$KP" --at "$P0" --mutate=shift >> "$OUT/logs/plant_check.log" 2>&1; s="$s $?"
echo "plant_check, --mutate=shift exits: $s (0 1)" >> "$X"
(cd "$IS" && $PY argcount_samebits.py "$IN/m3/points_M3_r0.18.jsonl" "$C") > "$OUT/logs/samebits.log" 2>&1
echo "samebits recount3 -> loc018 exit $? (0)" >> "$X"
echo "end $(date -u '+%F %T')" >> "$X"
exit
}
