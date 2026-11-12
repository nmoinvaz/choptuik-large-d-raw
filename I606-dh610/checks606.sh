#!/bin/bash
# #606: the checks of dh610's build of main, run after hp/build.sh. Logs go to I606-dh610/ of the raw clone.
set -u
REPO=/home/nathan/Source/choptuik-large-d
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I606-dh610
MAC=$RAW/I523-mac/c3
source $REPO/.venv/bin/activate
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2

# wait for the build, and stop unless it exited 0
while [ ! -e $OUT/build.end ]; do sleep 20; done
if ! tail -n 1 $OUT/build.log | grep -qx 'exit 0'; then echo "build failed, checks not run" | tee $OUT/checks_aborted.txt; exit 1; fi

# run NAME CMD...: header, output and exit status in OUT/NAME.log
run() {
    local name=$1; shift
    echo "== $name $(date -u +%H:%M) $*" > $OUT/$name.log
    "$@" >> $OUT/$name.log 2>&1
    local rc=$?
    echo "exit $rc" >> $OUT/$name.log
    echo "$name exit $rc" >> $OUT/exits.txt
}

cd $REPO
{
    echo "date $(date -u '+%Y-%m-%d %H:%M')  main $(git rev-parse --short HEAD)"
    python -c "import numpy, scipy, mpmath, sympy, flint, hpkernel, multidouble; print('numpy', numpy.__version__, 'scipy', scipy.__version__, 'mpmath', mpmath.__version__, 'sympy', sympy.__version__, 'python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__); print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa())"
    python --version; maturin --version; rustc --version; cargo --version; clang --version | head -1
    pip freeze | grep -i -E 'numpy|scipy|openblas|multidouble|hpkernel|flint'
    python -c "import numpy; numpy.show_config()" 2>&1 | grep -i -E 'name|version|openblas' | head -8
} > $OUT/versions.txt 2>&1
run import python -c "import numpy, scipy, mpmath, sympy, flint, hpkernel; print('imports ok', flint.__version__, flint.__FLINT_VERSION__)"

chain_selftest() { run selftest python check_numbers.py --selftest; }
chain_ref() {
    cd $REPO/hp
    run ref nice -n 10 python highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
    run scaled nice -n 10 python highm_check.py scaled --compare=$RAW/T81/scaled_main.json
}
chain_jets() {
    cd $REPO/hp
    run jets nice -n 10 python highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
    run jets_mutate_kappa nice -n 10 python highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
}
chain_bits() {
    cd $REPO/hp
    run bits_dump nice -n 10 python xsolve_bits.py dump $RAW $OUT/bits.json
    run bitsperturb_dump nice -n 10 python xsolve_bits.py dump $RAW $OUT/bits_perturb.json --perturb
    run bits_vs_mac python xsolve_bits.py compare $OUT/bits.json $MAC/bits.json
    run bitsperturb_vs_mac python xsolve_bits.py compare $OUT/bits_perturb.json $MAC/bits_perturb.json
    run bitsperturb_vs_own_unperturbed python xsolve_bits.py compare $OUT/bits_perturb.json $OUT/bits.json
}
chain_api() {
    cd $REPO/hp
    run api_dump nice -n 10 python api_bits.py dump $REPO/hp $RAW $OUT/api.json
    run apiperturb_dump nice -n 10 python api_bits.py dump $REPO/hp $RAW $OUT/api_perturb.json --perturb
    run api_vs_mac python api_bits.py compare $OUT/api.json $MAC/api.json
    run apiperturb_vs_mac python api_bits.py compare $OUT/api_perturb.json $MAC/api_perturb.json
    run apiperturb_vs_own_unperturbed python api_bits.py compare $OUT/api_perturb.json $OUT/api.json
}
chain_selftest & chain_ref & chain_jets & chain_bits & chain_api &
wait
date -u '+%Y-%m-%d %H:%M' > $OUT/checks.end
