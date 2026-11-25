#!/bin/bash
# the branch wip/large-d-form-s (with form S's Moebius horizon) as this machine's source tree fs/, its release build
# (build_fs.sh: low-memory recipe, 6 jobs), the wheel into site/ and the branch's Python files into hp/
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/refs/heads/wip/large-d-form-s | tar -xz -C "$T" --strip-components=1
grep -c "fn horizon_mob" "$T/hp/src/form_s.rs"
mkdir -p $HOME/.local/share/Trash/files
mv $W/fs $HOME/.local/share/Trash/files/fs_$(date +%s)
mv "$T" $W/fs
bash $W/build_fs.sh
bash $W/install_site.sh $W/fs
bash $W/update_py.sh
PYTHONPATH=$W/site $(cat $W/python_path) -c "from hpkernel._hpkernel import Solver; print('set_horizon_mobius', hasattr(Solver, 'set_horizon_mobius'))"
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
