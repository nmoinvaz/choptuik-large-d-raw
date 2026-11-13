#!/bin/bash
# The bit-identity checks of #599 for one build: run_checks.sh SITE OUTDIR STEP...
# steps: bits bitsperturb api apiperturb ref refmut scaled jets jetsmut prepfail
# Each step writes OUTDIR/<step>.log and ends it with "exit N". The references are the Mac's I523-mac/c3 files (main's
# hp/src at 1658a4f on multishoot 1.2.1) and T81's ref_main.json and scaled_main.json.
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a4f3680c95170e0c9/hp
RAW=$S/raw-i599
C3=$RAW/I523-mac/c3
SITE=$1
OUT=$2
shift 2
mkdir -p "$OUT"
cd "$HP" || exit 1
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
run() {
  local name=$1
  shift
  echo "== $name $(date -u '+%Y-%m-%d %H:%M') $*" > "$OUT/$name.log"
  PYTHONPATH=$SITE nice -n ${NICE:-10} "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
for step in "$@"; do
  case $step in
    bits)
      run bits_dump $PY xsolve_bits.py dump "$RAW" "$OUT/bits.json"
      run bits $PY xsolve_bits.py compare "$C3/bits.json" "$OUT/bits.json" ;;
    bitsperturb)
      run bitsperturb_dump $PY xsolve_bits.py dump "$RAW" "$OUT/bits_perturb.json" --perturb
      run bitsperturb $PY xsolve_bits.py compare "$C3/bits.json" "$OUT/bits_perturb.json" ;;
    api)
      run api_dump $PY api_bits.py dump "$HP" "$RAW" "$OUT/api.json"
      run api $PY api_bits.py compare "$C3/api.json" "$OUT/api.json" ;;
    apiperturb)
      run apiperturb_dump $PY api_bits.py dump "$HP" "$RAW" "$OUT/api_perturb.json" --perturb
      run apiperturb $PY api_bits.py compare "$C3/api.json" "$OUT/api_perturb.json" ;;
    ref)
      run ref $PY highm_check.py ref --compare="$RAW/T81/ref_main.json" --Ms=48,64,80 ;;
    refmut)
      # the control of ref's comparison: the reference with M = 48's residual_hi hash reversed must fail it
      $PY -c "import json,sys; r=json.load(open(sys.argv[1])); r['48']['residual_hi']=r['48']['residual_hi'][::-1]; json.dump(r,open(sys.argv[2],'w'),indent=1)" "$RAW/T81/ref_main.json" "$OUT/ref_main_mutated.json"
      run refmut $PY highm_check.py ref --compare="$OUT/ref_main_mutated.json" --Ms=48,64,80 ;;
    scaled)
      run scaled $PY highm_check.py scaled --compare="$RAW/T81/scaled_main.json" ;;
    jets)
      run jets $PY highm_check.py jets --compare="$RAW/anm-mac/jets_inputs/jets_inputs.json" ;;
    jetsmut)
      # the control of jets: model.rs JET_MUT_KAPPA must make the comparison fail
      run jetsmut $PY highm_check.py jets --compare="$RAW/anm-mac/jets_inputs/jets_inputs.json" --mutate=kappa ;;
    prepfail)
      run prepfail $PY "$S/i599/prepfail.py" dump "$HP" "$RAW" "$OUT/prepfail.json" ;;
  esac
done
echo "all done $(date -u '+%H:%M')" > "$OUT/done_$(echo "$@" | tr ' ' '_')"
