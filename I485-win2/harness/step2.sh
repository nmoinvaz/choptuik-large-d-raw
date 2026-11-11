#!/usr/bin/env bash
# #485, the second harness: build commit $1 in D:/choptuik-bisect2 with 1dcde949's modecount_cx overlaid (patches named in $2, comma list: halpha), venv-bisect2, and classify it.
# Exit 0 good, 1 bad, 125 does not build, 200 other. Files in I485-win2: build_ov_<h>.log, step_ov_<h>.{json,log}, class_ov_<h>.txt, patches/ov_<h>.diff.
export VIRTUAL_ENV="C:/Users/nathan/Source/venv-bisect2"
export PATH="/c/Users/nathan/Source/venv-bisect2/Scripts:/c/Users/nathan/.cargo/bin:$PATH"
export CARGO_BUILD_JOBS=${CARGO_BUILD_JOBS:-4} RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
SP="C:/Users/nathan/AppData/Local/Temp/claude/e3626a297248d1d0/4494066f-6a45-4ea7-bf7b-bdc7ecb92330/scratchpad"
WT=/d/choptuik-bisect2; RAW=D:/choptuik-large-d-raw; R=/d/choptuik-large-d-raw/I485-win2
PY="$VIRTUAL_ENV/Scripts/python.exe"
C=$1; PATCHES=${2:-}; MODE=${3:-overlay}   # overlay: 1dcde949's modecount_cx laid over the commit; own: the commit's own modecount_cx
git -C $WT checkout -q -f --detach $C || exit 200
H=$(git -C $WT rev-parse --short=8 HEAD)
L=$R/build_ov_$H.log
cd $WT/hp || exit 200
{
echo "=== ov step $H (mode $MODE): $(git -C $WT log -1 --format='%ad %s' --date=short | cut -c1-110)  patches: ${PATCHES:-none}"
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
[ "$MODE" = overlay ] && { git -C $WT checkout 1dcde949 -- hp/modecount_cx || exit 200; }
rm -f modecount_cx/Cargo.lock
for p in ${PATCHES//,/ }; do "$PY" "$SP/patch_$p.py" modecount_cx/src/lib.rs || { echo "PATCH $p FAILED"; exit 200; }; done
git -C $WT diff --cached HEAD -- hp/modecount_cx > "$R/patches/ov_$H.diff"
git -C $WT diff HEAD -- hp/modecount_cx >> "$R/patches/ov_$H.diff"
echo "overlay diff: $(wc -l < "$R/patches/ov_$H.diff") lines, saved to patches/ov_$H.diff"
git -C $WT show e043be2:hp/modecount_build.sh > modecount_build_bisect.sh
"$PY" -m pip uninstall -y multidouble hpkernel 2>&1 | tail -n 2
RUSTFLAGS="-C target-cpu=native" nice -n 2 maturin build --release -i "$PY" --out "$WT/hp/dist_ov_$H" || { echo "BUILD FAILED hpkernel"; exit 125; }
"$PY" -m pip install --force-reinstall --no-deps "$WT"/hp/dist_ov_$H/hpkernel-0.1.0-cp312-*.whl || { echo "INSTALL FAILED hpkernel"; exit 125; }
MD=$(sed -n 's/.*"\(multidouble @ [^"]*\)".*/\1/p' pyproject.toml)
if [ -n "$MD" ]; then "$PY" -m pip install --force-reinstall --no-deps "$MD" || { echo "INSTALL FAILED multidouble"; exit 125; }; else echo "pyproject.toml names no multidouble package at this commit"; fi
"$PY" -c "import hpkernel; print('hpkernel ok', hpkernel.isa())" || exit 125
bash modecount_build_bisect.sh || { echo "BUILD FAILED modecount_cx"; exit 125; }
echo "build done $(date -u '+%H:%M:%S UTC')"
} > "$L" 2>&1
rc=$?
if [ $rc -ne 0 ]; then echo "ov step $H: build failed (rc $rc)"; exit $([ $rc -eq 200 ] && echo 200 || echo 125); fi
S="$RAW/I250-mac/states/modecount_state_D30.0688_M48_october.npz"; E="$RAW/I250-mac/october/data/modecount_D30.0688_M48_october_evals.jsonl"
"$PY" "$RAW/I250-mac/scripts/fresh_vs_cache.py" "D:/choptuik-bisect2/hp" "$S" "$E" "$RAW/I485-win2/step_ov_$H.json" 4.267,0.9740000000000001 3.94364216362105,1.1900607986722187 > "$R/step_ov_$H.log" 2>&1
"$PY" - "$R/step_ov_$H.json" "$H" > "$R/class_ov_$H.txt" <<'PYEOF'
import json, sys
h = sys.argv[2]
try:
    j = json.load(open(sys.argv[1]))
except Exception as e:
    print(f"{h} other no result json ({e})"); sys.exit(0)
cache = [-940.4586634457893, -965.1149263751369]; today = [-940.4586634376807, -965.1149263918375]
la = [r["lnabs"] for r in j["rows"]]
dc = [abs(a - b) for a, b in zip(la, cache)]; dt = [abs(a - b) for a, b in zip(la, today)]
cls = "good" if max(dc) <= 1e-12 else ("bad" if max(dt) <= 1e-12 else "other")
print(f"{h} {cls} lnabs {la[0]!r} {la[1]!r} |d cache| {dc[0]:.3e} {dc[1]:.3e} |d today| {dt[0]:.3e} {dt[1]:.3e}")
PYEOF
cat "$R/class_ov_$H.txt"
case "$(cut -d' ' -f2 "$R/class_ov_$H.txt")" in good) exit 0 ;; bad) exit 1 ;; *) exit 200 ;; esac
