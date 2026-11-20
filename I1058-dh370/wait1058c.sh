#!/usr/bin/env bash
# (8179068d build) wakes when #1058's four checks are done ('checks done' in exits_1058.txt), or a check script ends non-zero where it must be zero, or unit i1058c is inactive
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I1058-dh370/at8179068d || exit 9
while sleep 20; do
  grep -q 'checks done' exits_1058.txt && { echo "CHECKS DONE"; grep '^1058 check' exits_1058.txt; exit 0; }
  grep -E '^1058 check (ref|scaled|jets) exit [1-9]' exits_1058.txt && { echo "A CHECK FAILED"; exit 0; }
  [ "$(systemctl --user is-active i1058c)" = active ] || { echo "UNIT i1058c NOT ACTIVE"; tail -n 3 exits_1058.txt; exit 0; }
done
