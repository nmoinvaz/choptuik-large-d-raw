#!/bin/bash
# #1025 winb, k_c 143 lane: dry tests of the scan driver (it starts hours after the regrid), written to selftest_scan_dry_1025.txt. Stand-ins (dry_stand_in, dry_empty, dry_badblob in this folder) hold win2's k_c 135 files
# under the k_c 143 names (the driver only checks blobs, the marker and the tool/ellrs selftests in a dry run). Nothing is started by the driver in --dry.
S=/c/Users/nathan/Source/kc143d23_1025
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
O=$S/selftest_scan_dry_1025.txt
cd "$S"
mkdir -p dry_stand_in dry_empty dry_badblob
SB=$(git hash-object --no-filters inputs/sol_l1kc135win2d23_D23.0000.npy); RB=$(git hash-object --no-filters inputs/l1kc135win2d23.jsonl)
for d in dry_stand_in dry_badblob; do
  cp inputs/sol_l1kc135win2d23_D23.0000.npy $d/sol_l1kc143winbd23_D23.0000.npy
  cp inputs/l1kc135win2d23.jsonl $d/l1kc143winbd23.jsonl
done
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "$SB" "$RB" > dry_stand_in/regrid_accepted.txt
printf 'ACCEPTED 2026-11-27 00:00:00 UTC\nstate %s\nrecord %s\n' "0000000000000000000000000000000000000000" "$RB" > dry_badblob/regrid_accepted.txt
export PYTHONDONTWRITEBYTECODE=1
: > "$O"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC dry tests of kc143d23_scan_driver_1025.py (stand-ins: win2's k_c 135 files under the k_c 143 names)" >> "$O"
t() {
  local n=$1 want=$2 label=$3; shift 3
  local t0=$(date +%s)
  "$PY" -u kc143d23_scan_driver_1025.py "$@" > "$S/dry_tmp.txt" 2>&1; local rc=$?
  { echo "== test $n: $label: exit $rc (wanted $want), $(( $(date +%s) - t0 )) s"; grep -E "REFUSE|DRY|exit 0 and|exit 1, 1|pins|usage|selftest exit" "$S/dry_tmp.txt" | cut -c1-330; } >> "$O"
}
t 1 0 "good stand-in, shares 0.055,0.050;0.060,0.055" "0.055,0.050;0.060,0.055" --dry --out=$S/dry_stand_in
t 2 0 "no marker (dry: logs REFUSE, continues, starts nothing)" "0.055,0.050;0.060,0.055" --dry --out=$S/dry_empty
t 3 0 "wrong state blob in the marker (dry: logs REFUSE)" "0.055,0.050;0.060,0.055" --dry --out=$S/dry_badblob
t 4 2 "one value only (refused)" "0.055" --dry --out=$S/dry_stand_in
t 5 2 "three shares (refused: at most two processes)" "0.05;0.055;0.06" --dry --out=$S/dry_stand_in
t 6 2 "a value three times (refused)" "0.055,0.055,0.055;0.06" --dry --out=$S/dry_stand_in
t 7 2 "--out without --dry (refused)" "0.055,0.050;0.060,0.055" --out=$S/dry_stand_in
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$O"
mv "$S/dry_tmp.txt" /c/Users/nathan/Source/_trash_1025/kc143_dry_tmp.txt
