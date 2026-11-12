#!/usr/bin/env bash
# #600: the bit-identity checks of #523 on win2, as I523-mac/run_checks.sh ran them on the Mac, for the build in venv-i600 (hp at main fc697f3a: hpkernel on multishoot 1.2.1, the exact projector).
# usage: run_600.sh STEP...   steps: bits bitsperturb api apiperturb ref scaled jets jetsmut
# Each step writes <OUT>/<step>.log and ends it with "exit N". The dumps go to <OUT>/bits_win.json, bits_win_perturb.json, api_win.json, api_win_perturb.json.
# RAWDIR is a worktree of origin/main of the raw-data repository (D:/choptuik-large-d-raw-push): it holds the Mac's references (I523-mac/c3/, T81/, anm-mac/jets_inputs/) and the stored states
# the checks read; the live clone is not pulled. The outputs go to the live clone's I600-win2/.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
HP=/d/choptuik-i600/hp
RAW=/d/choptuik-large-d-raw-push
OUT=/d/choptuik-large-d-raw/I600-win2
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 PYTHONFAULTHANDLER=1
cd "$HP" || exit 1
run() {
  local name=$1
  shift
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" > "$OUT/$name.log"
  "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
for step in "$@"; do
  case $step in
    bits)
      run bits_dump $PY xsolve_bits.py dump $RAW "$OUT/bits_win.json"
      run bits $PY xsolve_bits.py compare $RAW/I523-mac/c3/bits.json "$OUT/bits_win.json" ;;
    bitsperturb)
      run bitsperturb_dump $PY xsolve_bits.py dump $RAW "$OUT/bits_win_perturb.json" --perturb
      run bitsperturb $PY xsolve_bits.py compare "$OUT/bits_win.json" "$OUT/bits_win_perturb.json" ;;
    api)
      run api_dump $PY $RAW/I523-mac/api_bits.py dump "$HP" $RAW "$OUT/api_win.json"
      run api $PY $RAW/I523-mac/api_bits.py compare $RAW/I523-mac/c3/api.json "$OUT/api_win.json" ;;
    apiperturb)
      run apiperturb_dump $PY $RAW/I523-mac/api_bits.py dump "$HP" $RAW "$OUT/api_win_perturb.json" --perturb
      run apiperturb $PY $RAW/I523-mac/api_bits.py compare "$OUT/api_win.json" "$OUT/api_win_perturb.json" ;;
    ref)
      run ref $PY highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80 ;;
    scaled)
      run scaled $PY highm_check.py scaled --compare=$RAW/T81/scaled_main.json ;;
    jets)
      run jets $PY highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json ;;
    jetsmut)
      run jetsmut $PY highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa ;;
  esac
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" > "$OUT/done_$(echo "$@" | tr ' ' '_')"
