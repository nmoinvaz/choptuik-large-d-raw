#!/bin/bash
# #855's bit-identity checks on the 7e4cfd03 build, six chains in parallel, nice 10, no memory guard.
# References: T81, anm-mac, the Mac's I523-mac/c3 dumps and dh370's I614-dh370 dumps (main 3c35f0c: multishoot 1.2.2,
# multidouble 4.2.1), extracted by build.sh into $REF. States are read from dh610's raw clone.
WT=/home/nathan/Source/choptuik-large-d-855
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I855-dh610
REF=/home/nathan/scratch855/refs
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"
  nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
chain_ref()    { run ref python highm_check.py ref --compare=$REF/T81/ref_main.json --Ms=48,64,80; }
chain_scaled() { run scaled python highm_check.py scaled --compare=$REF/T81/scaled_main.json; }
chain_jets()   { J=$REF/anm-mac/jets_inputs/jets_inputs.json
                 run jets python highm_check.py jets --compare=$J
                 run jets_mutate_kappa python highm_check.py jets --compare=$J --mutate=kappa; }
chain_xs()     { run bits_dump python xsolve_bits.py dump $RAW "$OUT/bits.json"
                 run bits_vs_614 python xsolve_bits.py compare $REF/I614-dh370/bits.json "$OUT/bits.json"
                 run bits_vs_mac python xsolve_bits.py compare $REF/I523-mac/c3/bits.json "$OUT/bits.json"
                 run bitsperturb_dump python xsolve_bits.py dump $RAW "$OUT/bits_perturb.json" --perturb
                 run bitsperturb_vs_614 python xsolve_bits.py compare $REF/I614-dh370/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_vs_mac python xsolve_bits.py compare $REF/I523-mac/c3/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_control python xsolve_bits.py compare "$OUT/bits.json" "$OUT/bits_perturb.json"; }
chain_api()    { run api_dump python api_bits.py dump "$WT/hp" $RAW "$OUT/api.json"
                 run api_vs_614 python api_bits.py compare $REF/I614-dh370/api_nan1.json "$OUT/api.json"
                 run api_vs_mac python api_bits.py compare $REF/I523-mac/c3/api.json "$OUT/api.json"
                 run apiperturb_dump python api_bits.py dump "$WT/hp" $RAW "$OUT/api_perturb.json" --perturb
                 run apiperturb_vs_614 python api_bits.py compare $REF/I614-dh370/api_perturb_nan1.json "$OUT/api_perturb.json"
                 run apiperturb_vs_mac python api_bits.py compare $REF/I523-mac/c3/api_perturb.json "$OUT/api_perturb.json"
                 run apiperturb_control python api_bits.py compare "$OUT/api.json" "$OUT/api_perturb.json"; }
chain_mc()     { S=data/states/up2_D20.0437.npz
                 run modecount_check python modecount_check.py $S --quick --out="$OUT/modecount_check.jsonl"
                 run modecount_check_mutate_dmat python modecount_check.py $S --quick --mutate=dmat --out="$OUT/modecount_check.jsonl"; }
chain_ref & chain_scaled & chain_jets & chain_xs & chain_api & chain_mc &
wait
echo "all chains done $(date -u '+%H:%M')" > "$OUT/checks_done.txt"
