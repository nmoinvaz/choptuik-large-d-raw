#!/bin/bash
# after the D 300 release (unit i1088a-rls300): wip/large-d-form-s's hp sources (form S's Moebius horizon), the release
# build (build1088.sh: low-memory recipe, 10 jobs), the wheel into site/, the branch's Python files; then mobcheck at
# the D 400 held state (#1088's checks 1-3 of the Moebius port), 10 threads
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-rls300; do sleep 30; done
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/refs/heads/wip/large-d-form-s | tar -xz -C "$T" --strip-components=1
grep -c "fn horizon_mob" "$T/hp/src/form_s.rs"
cp "$T"/hp/src/*.rs $W/hp/src/
cp "$T"/hp/Cargo.toml $W/hp/Cargo.toml
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
bash $W/build1088.sh
bash $W/install_site.sh
bash $W/update_py.sh
PY=$(cat $W/python_path)
PYTHONPATH=$W/site $PY -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'set_horizon_mobius')"
date -u "+built %Y-%m-%d %H:%M:%S UTC"
cd $W/hp
set +e
PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2 $PY -u form_s.py mobcheck $W/out/j400_held/jump_s_D400.0000.npz $W/out/mobcheck400 \
  --mob 8 --threads 10 --it_max 4 --allow_unraw > $W/out/mobcheck400.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC rc $?"
exit
}
