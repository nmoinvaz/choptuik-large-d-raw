#!/bin/bash
# The bit-identity checks of AGENTS.md for hp's multidouble bump 1.5.1 -> 1.7.0: main (1.5.1) built into ~/venv-main,
# feat/qd-solver rebuilt from crates.io 1.7.0 into ~/venv-qds, then highm_check.py ref and scaled, --save with main's
# build and --compare with the branch's.
set -x
R=~/Source/raw-T81
export CARGO_PROFILE_RELEASE_STRIP=false
(cd ~/Source/choptuik-large-d/hp && git log -1 --oneline && PATH=~/venv-main/bin:$PATH nice -n 10 bash build.sh) > $R/build_main.log 2>&1 || exit 1
(cd ~/Source/choptuik-qd-solver/hp && git log -1 --oneline && PATH=~/venv-qds/bin:$PATH nice -n 10 bash build.sh) > $R/build_qds.log 2>&1 || exit 1
cd ~/Source/choptuik-qd-solver/hp
nice -n 10 ~/venv-main/bin/python -u highm_check.py ref --save=$R/ref_main.json > $R/ref_save.log 2>&1
nice -n 10 ~/venv-qds/bin/python -u highm_check.py ref --compare=$R/ref_main.json > $R/ref_compare.log 2>&1; echo "ref compare exit $?" >> $R/ref_compare.log
nice -n 10 ~/venv-main/bin/python -u highm_check.py scaled --save=$R/scaled_main.json > $R/scaled_save.log 2>&1
nice -n 10 ~/venv-qds/bin/python -u highm_check.py scaled --compare=$R/scaled_main.json > $R/scaled_compare.log 2>&1; echo "scaled compare exit $?" >> $R/scaled_compare.log
