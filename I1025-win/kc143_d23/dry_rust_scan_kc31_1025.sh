#!/bin/bash
# #1025 winb, k_c 143 lane: end-to-end dry test of the scan tool's new flags before the real scan (it starts hours after the regrid): d18_secant.py scan (wip/ell1-rust-b12 d4b6b6ce) on the k_c 31 state of #1102
# (raw I1102-mac/in, blobs f07a8984 / e5a87ec5; inputs of my #1102 stage) at D 10.5, lambda 2.87 and 2.86, once with --b12=rust --b12_threads=2 (ellrs from the site, OPENBLAS_NUM_THREADS=1) and once with the default block
# (--b12=ddm); the two record files must agree in every field that does not depend on the clock (compare_dry_rust_kc31.py). Output folder: dry_rust_vs_ddm_kc31/ in this folder's I1025-win/kc143_d23.
S=/c/Users/nathan/Source/kc143d23_1025
WTM=/c/Users/nathan/Source/choptuik-i1102/solver/matter
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
IN=/c/Users/nathan/Source/i1102_1025/inputs
SITE=C:/Users/nathan/Source/i1102_1025/site
OUTD=$S/I1025-win/kc143_d23/dry_rust_vs_ddm_kc31
mkdir -p "$OUTD"
export RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 P4_WT_MATTER=C:/Users/nathan/Source/choptuik-i1102/solver/matter
cd "$WTM"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC start" > "$OUTD/dry_rust_vs_ddm_kc31.txt"
t0=$(date +%s)
PYTHONPATH=$SITE "$PY" -u d18_secant.py scan $IN/l1kc31r1025.jsonl $IN/sol_l1kc31r1025_D10.5000.npy 10.5 2.87,2.86 "$OUTD/scan_rust.jsonl" --pin=f07a8984,e5a87ec5 --b12=rust --b12_threads=2 > "$OUTD/scan_rust.log" 2>&1
echo "rust: exit $? ($(( $(date +%s) - t0 )) s)" >> "$OUTD/dry_rust_vs_ddm_kc31.txt"
t0=$(date +%s)
"$PY" -u d18_secant.py scan $IN/l1kc31r1025.jsonl $IN/sol_l1kc31r1025_D10.5000.npy 10.5 2.87,2.86 "$OUTD/scan_ddm.jsonl" --pin=f07a8984,e5a87ec5 > "$OUTD/scan_ddm.log" 2>&1
echo "ddm: exit $? ($(( $(date +%s) - t0 )) s)" >> "$OUTD/dry_rust_vs_ddm_kc31.txt"
"$PY" "$S/compare_dry_rust_kc31.py" "$OUTD/scan_rust.jsonl" "$OUTD/scan_ddm.jsonl" >> "$OUTD/dry_rust_vs_ddm_kc31.txt" 2>&1
echo "compare: exit $?" >> "$OUTD/dry_rust_vs_ddm_kc31.txt"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$OUTD/dry_rust_vs_ddm_kc31.txt"
