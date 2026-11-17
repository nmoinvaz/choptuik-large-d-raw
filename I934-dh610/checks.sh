#!/bin/bash
# #934's bit-identity checks on the cdb5a6bc build, six chains in parallel, nice 10, no memory guard. References: T81,
# anm-mac, and #855's dumps on this machine (I855-dh610), extracted by build.sh into $REF. States are read from
# dh610's raw clone. Exits non-zero when a check that must pass fails or a control that must fail passes.
taskset -cp 0-4 $$ > /dev/null  # 5 of the 20 CPUs: two chains use the rest
WT=/home/nathan/Source/choptuik-large-d-934
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
REF=/home/nathan/scratch934/refs
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
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
                 run bits_vs_855 python xsolve_bits.py compare $REF/I855-dh610/bits.json "$OUT/bits.json"
                 run bitsperturb_dump python xsolve_bits.py dump $RAW "$OUT/bits_perturb.json" --perturb
                 run bitsperturb_vs_855 python xsolve_bits.py compare $REF/I855-dh610/bits_perturb.json "$OUT/bits_perturb.json"
                 run bitsperturb_control python xsolve_bits.py compare "$OUT/bits.json" "$OUT/bits_perturb.json"; }
chain_api()    { run api_dump python api_bits.py dump "$WT/hp" $RAW "$OUT/api.json"
                 run api_vs_855 python api_bits.py compare $REF/I855-dh610/api.json "$OUT/api.json"
                 run apiperturb_dump python api_bits.py dump "$WT/hp" $RAW "$OUT/api_perturb.json" --perturb
                 run apiperturb_vs_855 python api_bits.py compare $REF/I855-dh610/api_perturb.json "$OUT/api_perturb.json"
                 run apiperturb_control python api_bits.py compare "$OUT/api.json" "$OUT/api_perturb.json"; }
chain_mc()     { S=data/states/up2_D20.0437.npz
                 run modecount_check python modecount_check.py $S --quick --out="$OUT/modecount_check.jsonl"
                 run modecount_check_mutate_dmat python modecount_check.py $S --quick --mutate=dmat --out="$OUT/modecount_check.jsonl"; }
chain_ref & chain_scaled & chain_jets & chain_xs & chain_api & chain_mc &
wait
rc() { tail -1 "$OUT/$1.log" | sed 's/exit //'; }
bad=0
for n in ref scaled jets bits_vs_855 bitsperturb_vs_855 api_vs_855 apiperturb_vs_855 modecount_check; do
  [ "$(rc $n)" = 0 ] || { echo "MUST PASS failed: $n (exit $(rc $n))" >> "$OUT/checks_done.txt"; bad=1; }
done
for n in jets_mutate_kappa bitsperturb_control apiperturb_control modecount_check_mutate_dmat; do
  [ "$(rc $n)" != 0 ] || { echo "CONTROL passed: $n" >> "$OUT/checks_done.txt"; bad=1; }
done
echo "all chains done $(date -u '+%H:%M'), verdict exit $bad" >> "$OUT/checks_done.txt"
exit $bad
