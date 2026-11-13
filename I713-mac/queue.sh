#!/bin/bash
# #713: the runs left after the 22:40 UTC stop of 2026-11-13, one at a time through run.sh, in the README's order.
# A run whose log already has its "exit N" line is not run again. The queue stops at the first run whose exit is not
# the one the criteria expect (a check 0, a control 1), and prints one line per run to stdout.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$D/.." && pwd)
S200=T138-win2/chain_o/anm_pin3_D200.0000.npz
S252=I603-win2/chain/anm_pin3_D252.6135.npz
PW=I603-win2/chain_nsr/pred_pin3_D254.4381.npz
REF200=1.695088752463841744241523971202762929113
S0="--threads 3 --switch 0 --reseed_o 3 --reseed_start pred"

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
run 1 s0_D200_mo $P $S200 $S0 --qd 0 --Delta_ref $REF200 --mutate_offset qd --out $D/s0_D200_mo
run 1 s0_D200_m10 $P $S200 $S0 --qd 0 --Delta_ref $REF200 --mutate 10 --out $D/s0_D200_m10
# amendment 1: the default-switch reference at D 252.6 runs its octo-double half alone. Its exit 0 is the fallback's
# condition (converged below 1e-40), and its Delta is REF252.
run 0 ref_D252 $P $S252 --threads 3 --reseed_o 3 --reseed_start pred --qd 0 --out $D/ref_D252
REF252=$(jq -r '.od.Delta' "$D/ref_D252.json")
run 0 s0_D252 $P $S252 $S0 --qd 0 --Delta_ref $REF252 --out $D/s0_D252
run 1 s0_D252_mo $P $S252 $S0 --qd 0 --Delta_ref $REF252 --mutate_offset qd --out $D/s0_D252_mo
run 1 s0_D252_m10 $P $S252 $S0 --qd 0 --Delta_ref $REF252 --mutate 10 --out $D/s0_D252_m10
W="octo_corrector.py wall $RAW $PW $S0 --held_o 1"
run 0 s0_wall $W --out $D/s0_wall
run 1 s0_wall_mo $W --mutate_offset qd --out $D/s0_wall_mo
run 1 s0_wall_m10 $W --mutate 10 --out $D/s0_wall_m10
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
