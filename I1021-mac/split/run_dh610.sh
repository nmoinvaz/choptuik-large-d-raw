#!/bin/bash
# boxes 11-31 of #1021's M = 3 recount at xi1 0.17 (argcount at 068913b4, --m3fix --retry): 4 jobs x 3 processes,
# each from the Mac's cache split/points_M3_r0.17_in.jsonl (617 lines, every #1013 point included) into its own folder
#   run_dh610.sh CODE PY RAW    CODE: a choptuik-large-d worktree at 068913b4; PY: python; RAW: the raw clone's root
set -u
CODE=$1; PY=$2; RAW=$3
IN=$RAW/I1021-mac
OUT=$RAW/I1021-dh610
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 068913b45669b01c74d5dbcba628f3b752d26d3a ] || { echo "CODE is not at 068913b4"; exit 1; }
mkdir -p "$OUT/logs"
[ -f "$OUT/README.md" ] || printf '%s\n' "# I1021-dh610: boxes 11-31 of #1021's M = 3 recount at xi1 0.17 (argcount 068913b4, --m3fix --retry)" "" \
  "Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021." "" \
  "Inputs from I1021-mac/split/ (run_dh610.sh, leaves_b*.jsonl, points_M3_r0.17_in.jsonl) and I1021-mac/m3/points_M3_r0.2.jsonl." \
  "One folder per job, b11-15 b16-20 b21-25 b26-31. xfchecks merges them into I1021-mac's records." > "$OUT/README.md"
: > "$OUT/logs/exits.txt"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ echo "start $(date -u '+%F %T') $(uname -srm)"; $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$OUT/logs/exits.txt"
nice -n 10 $PY -u argcount.py --selftest > "$OUT/logs/selftest.log" 2>&1; s=$?; echo "selftest exit $s" >> "$OUT/logs/exits.txt"
[ $s = 0 ] || exit 1
for b in 11-15 16-20 21-25 26-31; do
  mkdir -p "$OUT/b$b"
  cp "$IN/split/points_M3_r0.17_in.jsonl" "$OUT/b$b/points_M3_r0.17.jsonl"
  cp "$IN/m3/points_M3_r0.2.jsonl" "$OUT/b$b/points_M3_r0.2.jsonl"
  ( nice -n 10 timeout 24h $PY -u argcount.py --M=3 --recount="$IN/split/leaves_b$b.jsonl" --r1=0.17 --r1b=0.2 \
      --seed="$OUT/b$b/points_M3_r0.2.jsonl" --m3fix --retry --procs=3 --out="$OUT/b$b" --tag="M3_cand_r0.17_fix_b$b" \
      > "$OUT/logs/recount_b$b.log" 2>&1
    echo "b$b exit $? $(date -u '+%F %T')" >> "$OUT/logs/exits.txt" ) &
done
wait
echo "end $(date -u '+%F %T')" >> "$OUT/logs/exits.txt"
