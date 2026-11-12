#!/bin/bash
WT=/home/nathan/Source/choptuik-large-d-604
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I604-dh370
cd "$WT/hp" && . ../.venv/bin/activate
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() { local name=$1; shift; echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"; nice -n 10 "$@" >> "$OUT/$name.log" 2>&1; echo "exit $?" >> "$OUT/$name.log"; }
chain1() { run api_nan1_dump python $OUT/api_bits_nan1.py dump "$WT/hp" $RAW "$OUT/api_nan1.json"
           run api_nan1_vs_mac python $RAW/I523-mac/api_bits.py compare $RAW/I523-mac/c3/api.json "$OUT/api_nan1.json"; }
chain2() { run apiperturb_nan1_dump python $OUT/api_bits_nan1.py dump "$WT/hp" $RAW "$OUT/api_perturb_nan1.json" --perturb
           run apiperturb_nan1_vs_mac python $RAW/I523-mac/api_bits.py compare $RAW/I523-mac/c3/api_perturb.json "$OUT/api_perturb_nan1.json"
           run apiperturb_nan1_control python $RAW/I523-mac/api_bits.py compare "$OUT/api_nan1.json" "$OUT/api_perturb_nan1.json"; }
chain1 & chain2 &
wait
echo "done $(date -u '+%H:%M')" > "$OUT/nan_done.txt"
