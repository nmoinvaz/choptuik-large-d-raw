#!/bin/bash
# wip/large-d-form-s's hp sources (4a0409b5 or later: HP_SLAVE_REFINE_QD/OD, form S at M 48, the magnitude hook) into
# hp/src, the release build (low-memory recipe, 4 jobs beside the running units), the wheel unpacked into site_r/ (a new
# folder: site/ stays as it is for the running jobs, which have its module mapped)
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/refs/heads/wip/large-d-form-s | tar -xz -C "$T" --strip-components=1
grep -c "HP_SLAVE_REFINE_OD" "$T/hp/src/form_s.rs"
cp "$T"/hp/src/*.rs $W/hp/src/
cp "$T"/hp/Cargo.toml $W/hp/Cargo.toml
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
cd $W/hp
export RUSTFLAGS="-C target-cpu=native" CARGO_TARGET_DIR=$W/target CARGO_BUILD_JOBS=4 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
/home/nathan/Source/venv-i1058/bin/maturin build --release -i /home/nathan/Source/venv-i1058/bin/python --out $W/dist_r
cd $W
PY=$(cat $W/python_path)
mkdir -p site_r
WHL=$(ls -t dist_r/hpkernel-*.whl | head -1)
$PY -m zipfile -e "$WHL" site_r/
cp $W/hp/python/hpkernel/__init__.py $W/hp/python/hpkernel/driver.py site_r/hpkernel/
PYTHONPATH=$W/site_r $PY -c "import hpkernel; from hpkernel._hpkernel import Solver; print(hpkernel.__file__)"
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
