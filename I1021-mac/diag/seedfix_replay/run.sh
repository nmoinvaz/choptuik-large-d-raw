#!/bin/bash
# #1021: replay the seeds of every M = 3 cache that ran with --seed (the 0.2 file) before 6da7da7b, with the copies as
# that code made them (no 'fix') and as 6da7da7b makes them (--keepfix); a point whose two seeds differ was seeded
# differently because of the seed bug. Control: box 16's relocation at 998fd290 (loc/z16), whose first seed must
# differ. Usage: run.sh RAW_I1021_MAC DH610_I1021 CODE PY
R=$1; N=$2; C=$3; PY=$4; W=$R/diag/seedfix_replay
set -e
cd "$W"
rp() { nice -n 19 "$PY" "$R/diag/replay_runs.py" "$C" "$@"; }
for k in "" --keepfix; do
  t=${k:+_keepfix}
  rp "$R/loc/z16/points_M3_r0.17.jsonl" "$R/loc/in/b16-20_points_M3_r0.17.jsonl" 951 1 "$W/control_z16$t.jsonl" 0:"$R/loc/leaf_z16.jsonl" $k
  rp "$R/m3/points_M3_r0.17.jsonl" "$R/m3/points_M3_r0.2.jsonl" 1026 2 "$W/mac$t.jsonl" 214:"$R/m3/leaves_M3_cand_r0.25.jsonl" 627:"$R/split/leaves_b07-10.jsonl" $k
  for b in b11-15 b16-20; do
    rp "$N/$b/points_M3_r0.17.jsonl" "$N/$b/points_M3_r0.2.jsonl" 1026 3 "$W/$b$t.jsonl" 617:"$R/split/leaves_$b.jsonl" $k
  done
  rp "$N/b21-25/points_M3_r0.17.jsonl" "$N/b21-25/points_M3_r0.2.jsonl" 1026 3 "$W/b21-25$t.jsonl" 617:"$R/split/leaves_b21-25.jsonl" 665:"$R/split/leaves_b21-25.jsonl" $k
  rp "$N/b26-31/points_M3_r0.17.jsonl" "$N/b26-31/points_M3_r0.2.jsonl" 1026 3 "$W/b26-31$t.jsonl" 617:"$R/split/leaves_b26-31.jsonl" 767:"$R/split/leaves_b26-31.jsonl" $k
done
