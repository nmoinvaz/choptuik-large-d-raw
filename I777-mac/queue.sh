#!/bin/bash
# #777 (the coordinator, 2026-11-14): newton_od's full_drop with the default own test, f = 1e-6, in this order; the
# queue stops at the first unexpected exit. Expected exits are fixed before any run.
#   toy        newton_od_toy.py: 0; its control --mutate=drop: 1
#   fixA, fixB #752's crawling iterate (I752-mac/R/crawl_iter_D118.0000_s1.npz), crawl_probe fixrun --switch 0 --accept own,
#              6 steps, on the old build: A without the option (it crawls: lam 1/2 at step 1, so it does not reach 1e-60
#              in 6 steps; exit 1), B with --full_drop 1e-6 (converges to 1e-60 within 6 steps; exit 0)
#   C2         #713's two-seed test at D 252.6 at switch 0 on the new build, now with --full_drop 1e-6: each seed exits 0
#              (pinned max|F| below 1e-40) and the seeds agree in Delta to 1e-30; then its two controls exit 1
#   D200       #713's s0_D200 with --full_drop 1e-6 against s0_D200's Delta (planted's own bar): exit 0
#   wall       #713's C3 at D 254.4 with --full_drop 1e-6: exit 0; its two controls exit 1
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$D/.." && pwd)
S252=I603-win2/chain/anm_pin3_D252.6135.npz
S200=T138-win2/chain_o/anm_pin3_D200.0000.npz
PW=I603-win2/chain_nsr/pred_pin3_D254.4381.npz
IT=$RAW/I752-mac/R/crawl_iter_D118.0000_s1.npz
FD="--full_drop 1e-6"
S0="--threads 3 --switch 0 --reseed_o 3 --reseed_start pred"
PY=/Users/nathan/venv-314/bin/python3

run() {   # run WANT NAME BUILD ARGS...
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

run 0 toy old newton_od_toy.py
run 1 toy_mutate_drop old newton_od_toy.py --mutate=drop
F="crawl_probe.py fixrun $RAW $IT --threads 3 --switch 0 --accept own --steps 6"
run 1 fixA old $F --out $D/fixA
run 0 fixB old $F $FD --out $D/fixB
P="octo_corrector.py planted $RAW"
run 0 s0_D252 new $P $S252 $S0 --qd 0 $FD --out $D/s0_D252
run 0 s0_D252_seed2 new $P $S252 $S0 --qd 0 --seed 2 $FD --out $D/s0_D252_seed2
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
run 1 s0_D252_mo new $P $S252 $S0 --qd 0 $FD --Delta_ref $REF252 --mutate_offset qd --out $D/s0_D252_mo
run 1 s0_D252_m10 new $P $S252 $S0 --qd 0 $FD --Delta_ref $REF252 --mutate 10 --out $D/s0_D252_m10
REF200=$(jq -r '.od.Delta' "$RAW/I713-mac/s0_D200.json")
run 0 s0_D200 new $P $S200 $S0 --qd 0 $FD --Delta_ref $REF200 --out $D/s0_D200
W="octo_corrector.py wall $RAW $PW $S0 --held_o 1 $FD"
run 0 s0_wall new $W --out $D/s0_wall
run 1 s0_wall_mo new $W --mutate_offset qd --out $D/s0_wall_mo
run 1 s0_wall_m10 new $W --mutate 10 --out $D/s0_wall_m10
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
