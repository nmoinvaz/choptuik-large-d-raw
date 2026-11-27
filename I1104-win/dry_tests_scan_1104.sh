#!/bin/bash
# #1104 winb, kappa 0.5 stage: dry tests of the scan driver (it starts hours after the re-solve), written to selftest_scan_dry_1104.txt. Stand-ins (dry_stand_in, dry_empty, dry_badblob, dry_hasscan in this folder) hold my
# kappa 0.7 k_c 143 files under the kappa 0.5 names (the driver only checks blobs, the marker, the output names and the tool/ellrs selftests in a dry run). Nothing is started by the driver in --dry.
S=/c/Users/nathan/Source/k050d23_1104
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
O=$S/selftest_scan_dry_1104.txt
cd "$S"
mkdir -p dry_stand_in dry_empty dry_badblob dry_hasscan
SB=$(git hash-object --no-filters inputs/sol_l1kc143winbd23_D23.0000.npy); RB=$(git hash-object --no-filters inputs/l1kc143winbd23.jsonl)
for d in dry_stand_in dry_badblob dry_hasscan; do
  cp inputs/sol_l1kc143winbd23_D23.0000.npy $d/sol_l1kc143winbk050d23_D23.0000.npy
  cp inputs/l1kc143winbd23.jsonl $d/l1kc143winbk050d23.jsonl
done
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "$SB" "$RB" > dry_stand_in/regrid_accepted.txt
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "$SB" "$RB" > dry_hasscan/regrid_accepted.txt
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "0000000000000000000000000000000000000000" "$RB" > dry_badblob/regrid_accepted.txt
echo '{}' > dry_hasscan/scan_k050_D23_p0.jsonl
export PYTHONDONTWRITEBYTECODE=1
: > "$O"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC dry tests of k050d23_scan_driver_1104.py (stand-ins: my kappa 0.7 k_c 143 files under the kappa 0.5 names; the output folder is the real one, files with the suffix .dry)" >> "$O"
t() {
  local n=$1 want=$2 label=$3; shift 3
  local t0=$(date +%s)
  "$PY" -u k050d23_scan_driver_1104.py "$@" > "$S/dry_tmp.txt" 2>&1; local rc=$?
  { echo "== test $n: $label: exit $rc (wanted $want), $(( $(date +%s) - t0 )) s"; grep -E "REFUSE|DRY|exit 0 and|exit 1, 1|pins|usage|selftest exit|first " "$S/dry_tmp.txt" | cut -c1-360; } >> "$O"
}
t 1 0 "good stand-in, shares 0.095,0.080;0.110,0.125" "0.095,0.080;0.110,0.125" --dry --out=$S/dry_stand_in
t 2 0 "no marker (dry: logs REFUSE, continues, starts nothing)" "0.095,0.080;0.110,0.125" --dry --out=$S/dry_empty
t 3 0 "wrong state blob in the marker (dry: logs REFUSE)" "0.095,0.080;0.110,0.125" --dry --out=$S/dry_badblob
t 4 0 "a scan file p0 exists (dry: logs REFUSE)" "0.095,0.080;0.110,0.125" --dry --out=$S/dry_hasscan
t 5 2 "one value only (refused)" "0.095" --dry --out=$S/dry_stand_in
t 6 2 "three shares (refused: at most two processes)" "0.08;0.095;0.11" --dry --out=$S/dry_stand_in
t 7 2 "a value three times (refused)" "0.095,0.095,0.095;0.11" --dry --out=$S/dry_stand_in
t 8 2 "--out without --dry (refused)" "0.095,0.080;0.110,0.125" --out=$S/dry_stand_in
t 9 0 "the widening round: 0.065;0.140 --first=2 --window=0.065,0.14 (files p2, p3; the p0 of test 4 is not in this out dir; reader window 0.065 0.14)" "0.065;0.140" --first=2 --window=0.065,0.14 --dry --out=$S/dry_hasscan
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$O"
mv "$S/dry_tmp.txt" /c/Users/nathan/Source/_trash_1025/k050_dry_tmp.txt
