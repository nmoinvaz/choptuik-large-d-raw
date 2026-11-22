#!/usr/bin/env bash
# #1021 sheet check of rpi5's fu021 final cache (README.md): bash run.sh RAW PY WORK
# RAW a clone of choptuik-large-d-raw holding REV, PY the interpreter (numpy), WORK an empty scratch folder.
# Logs go to this script's folder. Exit codes are written to exits.txt in the README's order.
RAW=$1; PY=$2; WORK=$3
REV=${REV:-425ba356}
HERE=$(cd "$(dirname "$0")" && pwd)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
[ -d "$WORK" ] && [ -z "$(ls -A "$WORK")" ] || { echo "WORK must be an empty folder"; exit 2; }
git -C "$RAW" cat-file -e "$REV^{commit}" || { echo "$REV not in $RAW"; exit 2; }
FULL=$(git -C "$RAW" rev-parse "$REV^{commit}")
mkdir -p "$WORK/fu" "$WORK/rec" "$WORK/scripts"
get() { git -C "$RAW" show "$FULL:$1" > "$2" || exit 2; }
get I1021-rpi5/fu021/m3/points_M3_r0.17.jsonl "$WORK/fu/points_M3_r0.17.jsonl"
get I1021-rpi5/fu021/m3/leaves_M3_fu021_pass2_r0.17.jsonl "$WORK/fu/leaves_M3_fu021_pass2_r0.17.jsonl"
get I1021-rpi5/fu021/m3/count_M3_fu021_pass2_r0.17.json "$WORK/fu/count_M3_fu021_pass2_r0.17.json"
get I1021-mac/final/record/points_M3_r0.17.jsonl "$WORK/rec/points_M3_r0.17.jsonl"
get I1021-mac/diag/sheet_check.py "$WORK/scripts/sheet_check.py"
get I1021-mac/rpi5_fu021/prefix_keys.py "$WORK/scripts/prefix_keys.py"
CACHE=$WORK/fu/points_M3_r0.17.jsonl; LEAVES=$WORK/fu/leaves_M3_fu021_pass2_r0.17.jsonl
COUNT=$WORK/fu/count_M3_fu021_pass2_r0.17.json; RECORD=$WORK/rec/points_M3_r0.17.jsonl
SC=$WORK/scripts/sheet_check.py; PK=$WORK/scripts/prefix_keys.py
{ echo "raw commit $FULL"; echo "python $("$PY" -I -c 'import sys,numpy;print(sys.version.split()[0],"numpy",numpy.__version__)')"
  (cd "$WORK" && sha256sum fu/* rec/* scripts/* && wc -l fu/*.jsonl rec/*.jsonl); } > "$HERE/sha256.txt"

cd "$HERE" || exit 2
: > exits.txt
run() {   # run LOG CMD...: the command's stdout and stderr to LOG, its exit code to exits.txt
    local log=$1; shift
    nice -n 19 "$@" > "$log" 2>&1; local rc=$?
    echo "$log $rc" >> exits.txt
}
run sheet_leaves.log "$PY" -I "$SC" "$CACHE" "$LEAVES" --count "$COUNT"
run sheet_lines.log "$PY" -I "$SC" "$CACHE" lines
run sheet_lines_count.log "$PY" -I "$SC" "$CACHE" lines --count "$COUNT"
run sheet_lines_switch.log "$PY" -I "$SC" "$CACHE" lines --mutate=switch
run sheet_leaves_switch.log "$PY" -I "$SC" "$CACHE" "$LEAVES" --mutate=switch
run prefix_keys.log "$PY" -I "$PK" "$RECORD" "$CACHE"
run prefix_keys_edit.log "$PY" -I "$PK" "$RECORD" "$CACHE" --mutate=edit
run sheet_record_lines.log "$PY" -I "$SC" "$RECORD" lines
echo "exits (README order): $(awk '{printf "%s ", $2}' exits.txt)" | tee summary.txt
