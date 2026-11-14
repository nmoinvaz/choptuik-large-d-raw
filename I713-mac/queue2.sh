#!/bin/bash
# #713, amendment 2 (the coordinator, 2026-11-14 07:50 UTC). ref_D252, the default switch at D 252.6, crawled from
# 03:02 to 07:45 UTC: 7 Newton steps, max|F| 3.4e-12 -> 3.8e-16 at lam 1/128 to 1/4 (#700's crawl), so it cannot reach
# the 1e-40 its exit needs, and it was stopped (ref_D252.log, no exit line). The stored chain state's Delta cannot stand
# in for it: at D 200 ref_D200's Delta differs from its stored state's by 7.8e-18. So C2 becomes a two-seed test at
# switch 0: s0_D252 at seed 1 and seed 2 must each converge below 1e-40 and agree in Delta to 1e-30, and seed 1's
# Delta is REF252 for the controls. The distance to the stored state's Delta is printed, with no bar. At D 200, C1
# already showed switch 0 equal to the default switch where both converge (8.12e-54). The rest is queue.sh's.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$D/.." && pwd)
S252=I603-win2/chain/anm_pin3_D252.6135.npz
PW=I603-win2/chain_nsr/pred_pin3_D254.4381.npz
S0="--threads 3 --switch 0 --reseed_o 3 --reseed_start pred"
PY=/Users/nathan/venv-314/bin/python3

# run WANT NAME ARGS...: run.sh NAME ARGS..., unless NAME.log has its exit line, then compare its exit with WANT.
run() {
  want=$1
  name=$2
  shift 2
  if ! grep -q '^exit ' "$D/$name.log" 2>/dev/null; then
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC $name started"
    "$D/run.sh" "$name" "$@"
  fi
  got=$(grep '^exit ' "$D/$name.log" | tail -1 | cut -d' ' -f2)
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC $name exit $got (expected $want)"
  if [ "$got" != "$want" ]; then
    echo "stopped at $name"
    exit 1
  fi
}

P="octo_corrector.py planted $RAW"
run 0 s0_D252 $P $S252 $S0 --qd 0 --out $D/s0_D252
run 0 s0_D252_seed2 $P $S252 $S0 --qd 0 --seed 2 --out $D/s0_D252_seed2
# C2: the two seeds' Delta to 1e-30, and the distance to the stored state's Delta (reported only)
"$PY" -I - "$D" "$RAW/$S252" > "$D/c2_compare.txt" 2>&1 <<'PYEOF'
import json, sys, numpy as np, mpmath as mp
mp.mp.prec = 600
d, st = sys.argv[1], sys.argv[2]
a = mp.mpf(json.load(open(f"{d}/s0_D252.json"))["od"]["Delta"])
b = mp.mpf(json.load(open(f"{d}/s0_D252_seed2.json"))["od"]["Delta"])
z = np.load(st, allow_pickle=False)
s = mp.fsum(mp.mpf(float(z[k][-1])) for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in z.files)
ok = abs(a - b) <= mp.mpf("1e-30")
print(f"seed 1 - seed 2 = {mp.nstr(a - b, 5)}; bar 1e-30: {'met' if ok else 'NOT MET'}")
print(f"seed 1 - the stored state = {mp.nstr(a - s, 5)} (reported, no bar)")
print("exit", 0 if ok else 1)
sys.exit(0 if ok else 1)
PYEOF
c2=$?
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC c2_compare exit $c2 (expected 0)"
[ $c2 = 0 ] || { echo "stopped at c2_compare"; exit 1; }
REF252=$(jq -r '.od.Delta' "$D/s0_D252.json")
run 1 s0_D252_mo $P $S252 $S0 --qd 0 --Delta_ref $REF252 --mutate_offset qd --out $D/s0_D252_mo
run 1 s0_D252_m10 $P $S252 $S0 --qd 0 --Delta_ref $REF252 --mutate 10 --out $D/s0_D252_m10
W="octo_corrector.py wall $RAW $PW $S0 --held_o 1"
run 0 s0_wall $W --out $D/s0_wall
run 1 s0_wall_mo $W --mutate_offset qd --out $D/s0_wall_mo
run 1 s0_wall_m10 $W --mutate 10 --out $D/s0_wall_m10
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC queue2 done"
