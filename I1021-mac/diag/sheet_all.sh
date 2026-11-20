#!/bin/bash
# #1021: sheet_check.py over every stored M = 3 count (raw folders extracted under SHEETS, dh610's #1021 files under
# DH, the Mac's under MAC). Usage: sheet_all.sh SHEETS DH MAC
PY=/Users/nathan/venv-314/bin/python
D=$(cd "$(dirname "$0")" && pwd)
X=$1; DH=$2; MAC=$3
run() { $PY $D/sheet_check.py "$@"; echo "  exit $?"; }
A=$X/I1013-dh610/m3
echo "== #1013 (dh610)"
run $A/points_M3_r0.2.jsonl $A/leaves_M3_cand.jsonl --count $A/count_M3_cand.json
run $A/points_M3_r0.25.jsonl $A/leaves_M3_cand_r0.25.jsonl --count $A/count_M3_cand_r0.25.json
run $A/points_M3_r0.17.jsonl $A/leaves_M3_cand_r0.17.jsonl --count $A/count_M3_cand_r0.17.json
run $A/points_M3_r0.2.jsonl $A/leaves_pilot_known.jsonl --count $A/count_pilot_known.json
run $A/points_M3_r0.25.jsonl $A/leaves_pilot_r0.25.jsonl --count $A/count_pilot_r0.25.json
run $A/points_M3_r0.17.jsonl $A/leaves_pilot_r0.17.jsonl --count $A/count_pilot_r0.17.json
for r in 0.2 0.25; do run $A/points_M3_r$r.jsonl lines; done
B=$X/I1020-dh610/m3
echo "== #1020 (dh610)"
run $B/points_M3_r0.2.jsonl $B/leaves_M3_ext.jsonl --count $B/count_M3_ext.json
run $B/points_M3_r0.25.jsonl $B/leaves_M3_ext_r0.25.jsonl --count $B/count_M3_ext_r0.25.json
run $B/points_M3_r0.17.jsonl $B/leaves_M3_ext_r0.17.jsonl --count $B/count_M3_ext_r0.17.json
for n in control minus plus; do run $B/points_M3_r0.3.jsonl $B/leaves_reloc_$n.jsonl --count $B/count_reloc_$n.json; done
for n in minus plus; do run $B/points_M3_r0.35.jsonl $B/leaves_reloc2_$n.jsonl --count $B/count_reloc2_$n.json; done
run $B/points_M3_r0.3.jsonl $B/leaves_reloc2_newzero.jsonl --count $B/count_reloc2_newzero.json
for n in minus plus; do run $B/points_M3_r0.35.jsonl $B/leaves_reloc3_$n.jsonl --count $B/count_reloc3_$n.json; done
for r in 0.2 0.25 0.3 0.35; do run $B/points_M3_r$r.jsonl lines; done
echo "== #1021 Mac (boxes 0-10; boxes 0-6 have no leaves file, so lines)"
run $MAC/m3/points_M3_r0.17.jsonl $MAC/m3/leaves_M3_cand_r0.17_fix_b07-10.jsonl --count $MAC/m3/count_M3_cand_r0.17_fix_b07-10.json
run $MAC/m3/points_M3_r0.17.jsonl lines
run $MAC/m3/points_M3_r0.2.jsonl lines
echo "== #1021 dh610"
run $DH/b11-15/points_M3_r0.17.jsonl $DH/b11-15/leaves_M3_cand_r0.17_fix_b11-15.jsonl --count $DH/b11-15/count_M3_cand_r0.17_fix_b11-15.json
run $DH/b16-20/points_M3_r0.17.jsonl $DH/b16-20/leaves_M3_cand_r0.17_fix_b16-20.jsonl --count $DH/b16-20/count_M3_cand_r0.17_fix_b16-20.json
run $DH/b26-31/points_M3_r0.17.jsonl $DH/b26-31/leaves_M3_cand_r0.17_fix_b26-31_998fd290.jsonl --count $DH/b26-31/count_M3_cand_r0.17_fix_b26-31_998fd290.json
for b in b11-15 b16-20 b21-25 b26-31; do run $DH/$b/points_M3_r0.17.jsonl lines; done
echo "== #1013 rpi5 upper box (running, lines)"
run $X/I1013-rpi5-cap/m3/points_M3_r0.17.jsonl lines
echo "== #1021 z16 relocation box, 0.2 first"
run $MAC/loc/z16/points_M3_r0.17.jsonl $MAC/loc/z16/leaves_M3_loc_z16_998fd290.jsonl --count $MAC/loc/z16/count_M3_loc_z16_998fd290.json
echo "== controls (must exit 1)"
run $DH/b16-20/points_M3_r0.17.jsonl $DH/b16-20/leaves_M3_cand_r0.17_fix_b16-20.jsonl --mutate=switch
run $MAC/m3/points_M3_r0.17.jsonl lines --mutate=switch
