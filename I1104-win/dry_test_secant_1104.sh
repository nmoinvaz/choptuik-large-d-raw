#!/bin/bash
# #1104 winb, kappa 0.5 stage: dry test of the secant driver on a stand-in stage (the real one has no accepted state, scan or ends yet). The driver takes its folders from its own location (S = dirname), so a copy of it in
# dry_secant_stage/ with a copy of inputs/ and an I1104-win/ holding my kappa 0.7 k_c 143 files under the kappa 0.5 names, a marker, two scan files made of the lines of my k_c 143 kappa 0.7 scan (lambda 0.05 and 0.055; stand-in only)
# and the ends file (binary copy of two of their lines) runs its pins, the tool's selftest and controls, the three selftests and the acceptance runs (the kappa 0.5 gate must REFUSE the stand-in: the dry run logs it and prints the command).
# Output: selftest_secant_dry_1104.txt next to this script. Nothing is started by the driver in --dry.
S=/c/Users/nathan/Source/k050d23_1104
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
K143=/c/Users/nathan/Source/kc143d23_1025/I1025-win/kc143_d23
D=$S/dry_secant_stage
O=$S/selftest_secant_dry_1104.txt
mkdir -p "$D/I1104-win/secant" "$D/inputs"
cp "$S"/inputs/* "$D/inputs/"
cp "$S/k050d23_secant_driver_1104.py" "$D/"
T=$D/I1104-win
cp "$S/inputs/sol_l1kc143winbd23_D23.0000.npy" "$T/sol_l1kc143winbk050d23_D23.0000.npy"
cp "$S/inputs/l1kc143winbd23.jsonl" "$T/l1kc143winbk050d23.jsonl"
SB=$(git hash-object --no-filters "$T/sol_l1kc143winbk050d23_D23.0000.npy"); RB=$(git hash-object --no-filters "$T/l1kc143winbk050d23.jsonl")
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "$SB" "$RB" > "$T/regrid_accepted.txt"
cp "$K143/scan_kc143_D23_p0.jsonl" "$T/scan_k050_D23_p0.jsonl"
cp "$K143/scan_kc143_D23_p1.jsonl" "$T/scan_k050_D23_p1.jsonl"
cp "$K143/scan_kc143_D23_ends.jsonl" "$T/scan_k050_D23_ends.jsonl"
EB=$(git hash-object --no-filters "$T/scan_k050_D23_ends.jsonl")
export PYTHONDONTWRITEBYTECODE=1
cd "$D"
: > "$O"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC dry tests of k050d23_secant_driver_1104.py on dry_secant_stage (stand-in files)" >> "$O"
t() {
  local n=$1 want=$2 label=$3; shift 3
  local t0=$(date +%s)
  "$PY" -u k050d23_secant_driver_1104.py "$@" > "$S/dry_tmp2.txt" 2>&1; local rc=$?
  { echo "== test $n: $label: exit $rc (wanted $want), $(( $(date +%s) - t0 )) s"; cut -c1-520 "$S/dry_tmp2.txt"; } >> "$O"
}
t 1 0 "good stand-in, LO HI 0.05 0.055, ends blob right (the gate must refuse the kappa 0.7 stand-in; the dry run goes on)" 0.05 0.055 --ends-blob=$EB --dry
t 2 2 "no --ends-blob (usage)" 0.05 0.055 --dry
t 3 0 "wrong ends blob (dry: logs REFUSE)" 0.05 0.055 --ends-blob=0000000000000000000000000000000000000000 --dry
t 4 0 "LO HI not the ends' lambda (dry: logs REFUSE)" 0.045 0.055 --ends-blob=$EB --dry
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$O"
mv "$S/dry_tmp2.txt" /c/Users/nathan/Source/_trash_1025/k050_dry_tmp2.txt
