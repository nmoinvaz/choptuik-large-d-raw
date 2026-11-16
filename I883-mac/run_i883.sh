#!/bin/bash
# #883: lemma6b1_cover.py with --tag=_x, every command, while the stored run directory is renamed away, so that a
# read of the stored rows would fail. Usage: run_i883.sh <python> <output directory>, from solver/proof of the checkout.
PY=$1; OUT=$2
mkdir -p "$OUT"
[ -d lemma6b1_runs ] && [ ! -e lemma6b1_runs_x ] && [ ! -e lemma6b1_runs_away ] || { echo "STOP: unexpected run directories"; exit 9; }
shasum -a 256 lemma6b1_runs/* > "$OUT/stored_sha_before.txt"
mv lemma6b1_runs lemma6b1_runs_away
run() { local name=$1; shift; nice -n 10 "$PY" "$@" > "$OUT/$name.log" 2>&1; echo "$name: exit $?: python3 $*" | tee -a "$OUT/exits.txt"; }
run check_x_empty lemma6b1_cover.py check --tag=_x
run ray lemma6b1_cover.py ray --tag=_x
run rows lemma6b1_cover.py rows --tag=_x
run check lemma6b1_cover.py check --tag=_x --json="$OUT/check_x.json"
run check_drop lemma6b1_cover.py check --tag=_x --drop=5,6
run mutate_sign lemma6b1_cover.py --mutate=sign --tag=_x
run control lemma6b1_cover.py control --tag=_x --json="$OUT/control_x.json"
ls lemma6b1_runs_x > "$OUT/files_in_runs_x.txt"
ls -d lemma6b1_runs* > "$OUT/run_directories_during.txt"
mv lemma6b1_runs_away lemma6b1_runs
shasum -a 256 lemma6b1_runs/* > "$OUT/stored_sha_after.txt"
# with the stored rows back: a tagged rows run must not skip a row because the stored folder has it
mkdir lemma6b1_runs_y && cp lemma6b1_runs_x/ray.json lemma6b1_runs_y/
run rows_y_from11 lemma6b1_cover.py rows --from=11 --tag=_y
ls lemma6b1_runs_y > "$OUT/files_in_runs_y.txt"
shasum -a 256 lemma6b1_runs/* > "$OUT/stored_sha_after_y.txt"
# the untagged check on the stored rows, last
run check_stored lemma6b1_cover.py check
cat "$OUT/exits.txt"
