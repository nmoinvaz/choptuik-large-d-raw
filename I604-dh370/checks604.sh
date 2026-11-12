#!/bin/bash
# The #604 checks on dh370: five chains in parallel, each step logs to OUT/<name>.log and ends with "exit N".
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I604-dh370
cd "$WT/hp" && . ../.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"
  nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
chain_ref()    { run ref python highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80; }
chain_scaled() { run scaled python highm_check.py scaled --compare=$RAW/T81/scaled_main.json; }
chain_jets()   { J=$RAW/anm-mac/jets_inputs/jets_inputs.json
                 run jets python highm_check.py jets --compare=$J
                 run jets_mutate_kappa python highm_check.py jets --compare=$J --mutate=kappa; }
chain_xs()     { run bits_dump python xsolve_bits.py dump $RAW "$OUT/bits.json"
                 run bits_vs_mac python xsolve_bits.py compare $RAW/I523-mac/c3/bits.json "$OUT/bits.json"
                 run bitsperturb_dump python xsolve_bits.py dump $RAW "$OUT/bits_perturb.json" --perturb
                 run bitsperturb_vs_mac python xsolve_bits.py compare $RAW/I523-mac/c3/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_control python xsolve_bits.py compare "$OUT/bits.json" "$OUT/bits_perturb.json"; }
chain_api()    { A=$RAW/I523-mac/api_bits.py
                 run api_dump python $A dump "$WT/hp" $RAW "$OUT/api.json"
                 run api_vs_mac python $A compare $RAW/I523-mac/c3/api.json "$OUT/api.json"
                 run apiperturb_dump python $A dump "$WT/hp" $RAW "$OUT/api_perturb.json" --perturb
                 run apiperturb_vs_mac python $A compare $RAW/I523-mac/c3/api_perturb.json "$OUT/api_perturb.json"
                 run apiperturb_control python $A compare "$OUT/api.json" "$OUT/api_perturb.json"; }
chain_ref & chain_scaled & chain_jets & chain_xs & chain_api &
wait
echo "all chains done $(date -u '+%H:%M')" > "$OUT/checks_done.txt"
