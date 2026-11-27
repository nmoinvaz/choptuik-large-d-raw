#!/bin/bash
# #1025 macm3 kc143_d23125/rust_b12/gates.sh (t5's order, hc 04:23 UTC 27 Nov, #1102): gates 2 of 4 for ellrs (block 12 in Rust), worktree 1102m3 at d4b6b6ce, SITE ~/Source/ellrs-site-1102m3.
# Runs selftest (exit 0 wanted), selftest --mutate=nolam and --mutate=harm (exit 1 wanted each), and check on raw I1102-mac's k_c 31 state (in/, blobs e5a87ec5, f07a8984) at D 10.5, lambda 2.87,
# --threads=4 --controls=1 (exit 0 wanted: 15010 of 15010 bit for bit, both controls fail). Logs and exit codes to gate_*.txt; usage: bash gates.sh
H=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125/rust_b12
WT=$HOME/Source/choptuik-large-d-1102m3/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
export PYTHONPATH=$HOME/Source/ellrs-site-1102m3 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd $WT || exit 9
stamp() { date -u '+%F %T UTC'; }
[ "$(git rev-parse --short=8 HEAD)" = d4b6b6ce ] || { echo "worktree is not at d4b6b6ce"; exit 9; }
[ "$(git hash-object --no-filters ell_b12rs.py | cut -c1-8)" = "$(git rev-parse --short=8 d4b6b6ce:solver/matter/ell_b12rs.py)" ] || { echo "ell_b12rs.py differs from d4b6b6ce"; exit 9; }
echo "$(stamp) gates start: ell_b12rs.py $(git hash-object --no-filters ell_b12rs.py | cut -c1-8), $($PY -c 'import ellrs; print(ellrs.isa(), ellrs.gemm())')" > $H/gates_log.txt
run() { name=$1; shift; t0=$(date +%s); nice -n 15 "$@" > $H/gate_$name.txt 2>&1; e=$?; echo "$(stamp) $name: exit $e, wall $(( $(date +%s) - t0 )) s" >> $H/gates_log.txt; }
run selftest $PY ell_b12rs.py selftest
run selftest_nolam $PY ell_b12rs.py selftest --mutate=nolam
run selftest_harm $PY ell_b12rs.py selftest --mutate=harm
run check_kc31 $PY ell_b12rs.py check $H/in/l1kc31r1025.jsonl $H/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=4 --controls=1
echo "$(stamp) gates end" >> $H/gates_log.txt
