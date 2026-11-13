#!/bin/bash
# #614's bit-identity checks on the 3c35f0c build (dh370), five chains in parallel, nice 10, no memory guard.
# References: the stored files (T81, anm-mac), the Mac's I523-mac/c3 dumps, and dh370's own #604 build (main e835d94, I604-dh370/).
WT=/home/nathan/Source/choptuik-large-d-614
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I614-dh370
R604=$RAW/I604-dh370
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
                 run bits_vs_604 python xsolve_bits.py compare $R604/bits.json "$OUT/bits.json"
                 run bits_vs_mac python xsolve_bits.py compare $RAW/I523-mac/c3/bits.json "$OUT/bits.json"
                 run bitsperturb_dump python xsolve_bits.py dump $RAW "$OUT/bits_perturb.json" --perturb
                 run bitsperturb_vs_604 python xsolve_bits.py compare $R604/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_vs_mac python xsolve_bits.py compare $RAW/I523-mac/c3/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_control python xsolve_bits.py compare "$OUT/bits.json" "$OUT/bits_perturb.json"; }
chain_api()    { A=$RAW/I523-mac/api_bits.py; N=$R604/api_bits_nan1.py
                 run api_nan1_dump python $N dump "$WT/hp" $RAW "$OUT/api_nan1.json"
                 run api_nan1_vs_604 python $A compare $R604/api_nan1.json "$OUT/api_nan1.json"
                 run api_nan1_vs_mac python $A compare $RAW/I523-mac/c3/api.json "$OUT/api_nan1.json"
                 run apiperturb_nan1_dump python $N dump "$WT/hp" $RAW "$OUT/api_perturb_nan1.json" --perturb
                 run apiperturb_nan1_vs_604 python $A compare $R604/api_perturb_nan1.json "$OUT/api_perturb_nan1.json"
                 run apiperturb_nan1_vs_mac python $A compare $RAW/I523-mac/c3/api_perturb.json "$OUT/api_perturb_nan1.json"
                 run apiperturb_nan1_control python $A compare "$OUT/api_nan1.json" "$OUT/api_perturb_nan1.json"; }
chain_ref & chain_scaled & chain_jets & chain_xs & chain_api &
wait
echo "all chains done $(date -u '+%H:%M')" > "$OUT/checks_done.txt"
