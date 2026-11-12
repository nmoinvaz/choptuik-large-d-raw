#!/bin/bash
# The bit-identity checks of #523 for one build: run_checks.sh SITE OUTDIR STEP...
# steps: bitsperturb apibase api apiperturb ref jets jetsmut scaled planted wall wallmut
# Each step writes OUTDIR/<step>.log and ends it with "exit N".
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad
X=$S/xs
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a1d6c8d73638fe3f8/hp
RAW=$S/raw-i489
SITE=$1
OUT=$2
shift 2
mkdir -p "$OUT"
cd "$HP" || exit 1
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() {
  local name=$1
  shift
  echo "== $name $(date -u '+%H:%M') $*" > "$OUT/$name.log"
  PYTHONPATH=$SITE nice -n ${NICE:-10} "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
for step in "$@"; do
  case $step in
    bits)
      run bits_dump $PY xsolve_bits.py dump $S/rawc "$OUT/bits.json"
      run bits $PY xsolve_bits.py compare $X/bits_base.json "$OUT/bits.json" ;;
    bitsperturb)
      run bitsperturb_dump $PY xsolve_bits.py dump $S/rawc "$OUT/bits_perturb.json" --perturb
      run bitsperturb $PY xsolve_bits.py compare $X/bits_base.json "$OUT/bits_perturb.json" ;;
    apibase)
      run apibase $PY $S/i523/api_bits.py dump "$HP" $S/rawc "$OUT/api_base.json" ;;
    api)
      run api_dump $PY $S/i523/api_bits.py dump "$HP" $S/rawc "$OUT/api.json"
      run api $PY $S/i523/api_bits.py compare "$OUT/../base/api_base.json" "$OUT/api.json" ;;
    apiperturb)
      run apiperturb_dump $PY $S/i523/api_bits.py dump "$HP" $S/rawc "$OUT/api_perturb.json" --perturb
      run apiperturb $PY $S/i523/api_bits.py compare "$OUT/../base/api_base.json" "$OUT/api_perturb.json" ;;
    ref)
      run ref $PY highm_check.py ref --compare=$X/ref_base.json --Ms=8,16,48,64,80,96 ;;
    jets)
      run jets $PY highm_check.py jets --compare=$X/jets_base.json ;;
    jetsmut)
      run jetsmut $PY highm_check.py jets --compare=$X/jets_base.json --mutate=kappa ;;
    scaled)
      run scaled $PY highm_check.py scaled --compare=$X/scaled_base.json ;;
    planted)
      run planted $PY octo_corrector.py planted ~/Source/choptuik-large-d-raw T129-win2/chain/anm_pin3_D180.5246.npz --threads 2 ;;
    wall)
      run wall $PY octo_corrector.py wall ~/Source/choptuik-large-d-raw T129-win2/chain2/pred_pin3_D194.2746.npz --threads 2 ;;
    wallmut)
      run wallmut $PY octo_corrector.py wall ~/Source/choptuik-large-d-raw T129-win2/chain2/pred_pin3_D194.2746.npz --threads 2 --mutate 10 ;;
  esac
done
echo "all done $(date -u '+%H:%M')" > "$OUT/done_$(echo "$@" | tr ' ' '_')"
