#!/bin/bash
# #1025 winb, k_c 143 lane: dry test of the secant driver on a stand-in stage (the real one has no accepted state, scan or ends yet). The driver takes its folders from its own location (S = dirname), so a copy of it in
# dry_secant_stage/ with a copy of inputs/ and an I1025-win/kc143_d23/ holding win2's k_c 135 files under the k_c 143 names, a marker, two scan files made of lines of my k_c 127 scan (lambda 0.04 and 0.05; stand-in only) and the
# ends file of their line 1s runs its pins, the tool's selftest and controls, the three selftests and the five acceptance runs (the k_c 143 check must REFUSE the stand-in: the dry run logs it and prints the command).
# Output: selftest_secant_dry_1025.txt next to this script. Nothing is started by the driver in --dry.
S=/c/Users/nathan/Source/kc143d23_1025
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
K127=/c/Users/nathan/Source/kc127d23_1025/I1025-win/kc127_d23
D=$S/dry_secant_stage
O=$S/selftest_secant_dry_1025.txt
mkdir -p "$D/I1025-win/kc143_d23/secant" "$D/inputs"
cp "$S"/inputs/* "$D/inputs/"
cp "$S/kc143d23_secant_driver_1025.py" "$D/"
T=$D/I1025-win/kc143_d23
cp "$S/inputs/sol_l1kc135win2d23_D23.0000.npy" "$T/sol_l1kc143winbd23_D23.0000.npy"
cp "$S/inputs/l1kc135win2d23.jsonl" "$T/l1kc143winbd23.jsonl"
SB=$(git hash-object --no-filters "$T/sol_l1kc143winbd23_D23.0000.npy"); RB=$(git hash-object --no-filters "$T/l1kc143winbd23.jsonl")
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "$SB" "$RB" > "$T/regrid_accepted.txt"
head -1 "$K127/scan_kc127_D23_p0.jsonl" > "$T/scan_kc143_D23_p0.jsonl"
head -1 "$K127/scan_kc127_D23_p1.jsonl" > "$T/scan_kc143_D23_p1.jsonl"
cat "$T/scan_kc143_D23_p0.jsonl" "$T/scan_kc143_D23_p1.jsonl" > "$T/scan_kc143_D23_ends.jsonl"
EB=$(git hash-object --no-filters "$T/scan_kc143_D23_ends.jsonl")
export PYTHONDONTWRITEBYTECODE=1
cd "$D"
: > "$O"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC dry tests of kc143d23_secant_driver_1025.py on dry_secant_stage (stand-in files)" >> "$O"
t() {
  local n=$1 want=$2 label=$3; shift 3
  local t0=$(date +%s)
  "$PY" -u kc143d23_secant_driver_1025.py "$@" > "$S/dry_tmp2.txt" 2>&1; local rc=$?
  { echo "== test $n: $label: exit $rc (wanted $want), $(( $(date +%s) - t0 )) s"; cut -c1-420 "$S/dry_tmp2.txt"; } >> "$O"
}
t 1 0 "good stand-in, LO HI 0.04 0.05, ends blob right (the acceptance runs must refuse the stand-in; the dry run goes on)" 0.04 0.05 --ends-blob=$EB --dry
t 2 2 "no --ends-blob (usage)" 0.04 0.05 --dry
t 3 0 "wrong ends blob (dry: logs REFUSE)" 0.04 0.05 --ends-blob=0000000000000000000000000000000000000000 --dry
t 4 0 "LO HI not the ends' lambda (dry: logs REFUSE)" 0.045 0.055 --ends-blob=$EB --dry
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$O"
mv "$S/dry_tmp2.txt" /c/Users/nathan/Source/_trash_1025/kc143_dry_tmp2.txt
