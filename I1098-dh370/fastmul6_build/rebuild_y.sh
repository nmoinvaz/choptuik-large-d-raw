#!/bin/bash
# fastmul6 ($1: its commit) on dh370 into hp_y/ (its own copy of hp), the release build with the low-memory recipe and 3
# jobs (31 GB here, about 6 GB of it held by the #1025 regrid; a memory log every 30 s in out/fastmul6_build/mem.log, alert
# only), the wheel unpacked into site_y/; then the four checks: relaxed_build_check (D 2000 step file), recip_check at
# D 300 and D 1000, dmat_check at D 300 and D 1000 (the 2c control inside), taylor_mp_check at D 300
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
V=/home/nathan/Source/choptuik-large-d-1082/.venv
C=$1
O=$W/out/fastmul6_build
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC"
( while true; do echo "$(date -u +%H:%M:%S) $(free -m | awk '/Mem:/ {print "used", $3, "avail", $7} /Swap:/ {print "swap", $3}' | tr '\n' ' ')" >> $O/mem.log; sleep 30; done ) &
MEMPID=$!
trap 'kill $MEMPID 2>/dev/null' EXIT
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/$C | tar -xz -C "$T" --strip-components=1
grep -c "fn dapply_c" "$T/hp/src/model.rs"
grep -c "floor_dz=1e-12" "$T/hp/form_s.py"
mkdir -p $W/hp_y
cp -r "$T"/hp/. $W/hp_y/
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
cd $W/hp_y
export RUSTFLAGS="-C target-cpu=native" CARGO_TARGET_DIR=$W/target_y CARGO_BUILD_JOBS=3 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
$V/bin/maturin build --release -i $V/bin/python --out $W/dist_y
cd $W
mkdir -p site_y
WHL=$(ls -t dist_y/hpkernel-*.whl | head -1)
$V/bin/python -m zipfile -e "$WHL" site_y/
cp $W/hp_y/python/hpkernel/__init__.py $W/hp_y/python/hpkernel/driver.py site_y/hpkernel/
PYTHONPATH=$W/site_y $V/bin/python -c "import hpkernel; from hpkernel._hpkernel import Solver; print(hpkernel.__file__, hasattr(Solver, 'set_dmat_corr'))"
date -u "+built %Y-%m-%d %H:%M:%S UTC"
kill $MEMPID
set +e
cd $W/hp_y
PY=$V/bin/python
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
I=$W/out/ladder/inputs
$PY -u relaxed_build_check.py $I/L2000_step.npz > $O/relaxed.log 2>&1; echo "relaxed_build_check exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $I/D300_full_base.npz --threads 4 > $O/recip300.log 2>&1; echo "recip_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $I/D1000_base.npz --threads 4 > $O/recip1000.log 2>&1; echo "recip_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $I/D300_full_base.npz > $O/dmat300.log 2>&1; echo "dmat_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $I/D1000_base.npz > $O/dmat1000.log 2>&1; echo "dmat_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u taylor_mp_check.py $I/D300_full_base.npz > $O/taylor300.log 2>&1; echo "taylor_mp_check D 300 exit=$?" >> $O/exit_codes.txt
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
