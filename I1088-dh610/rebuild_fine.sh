#!/bin/bash
# wip/large-d-form-s's hp sources (580af314 or later: path_s, jacobian_sub_s, the Moebius constants in the lane's
# precision, the z recurrence) into hp/src, the release build (build1088.sh: low-memory recipe, 10 jobs), the wheel into
# site/, the branch's Python files
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/refs/heads/wip/large-d-form-s | tar -xz -C "$T" --strip-components=1
grep -c "fn path_s_in" "$T/hp/src/form_s.rs"
cp "$T"/hp/src/*.rs $W/hp/src/
cp "$T"/hp/Cargo.toml $W/hp/Cargo.toml
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
bash $W/build1088.sh
bash $W/install_site.sh
bash $W/update_py.sh
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; assert hasattr(Solver, 'path_s') and hasattr(Solver, 'jacobian_sub_s')"
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
