#!/usr/bin/env bash
# P2 item 4 (#1061): every check, control and closure run, in order, one process at a time at nice 10.
# Run from choptuik-large-d/solver/proof/review_p2c with RAW set to this folder.
{
set -u
PY=/Users/nathan/venv-314/bin/python
run() { local name=$1; shift; echo "== $name: $* ($(date -u '+%Y-%m-%d %H:%M'))"; nice -n 10 $PY "$@" > "$RAW/$name.log" 2>&1; echo "   exit $?"; tail -2 "$RAW/$name.log"; }
run series_centre        p2c_b8_series.py --centre
run series_box           p2c_b8_series.py
run K1_series_atom       p2c_b8_series.py --centre --mutate=atom
run identities           p2c_b8_boot.py --check=identities
run K2_identities_rho2   p2c_b8_boot.py --check=identities --mutate=drop_rho2
run K2_identities_W2     p2c_b8_boot.py --check=identities --mutate=drop_W2
run instances            p2c_b8_boot.py --check=instances --L0=73.89
run K2_instances_rho2    p2c_b8_boot.py --check=instances --L0=73.89 --mutate=bound_rho2
run K2_instances_W2      p2c_b8_boot.py --check=instances --L0=73.89 --mutate=bound_W2
run insens_prodrule      p2c_b8_boot.py --check=instances --L0=73.89 --mutate=prodrule
run kernel               p2c_b8_boot.py --check=kernel
run K3_kernel_kappa      p2c_b8_boot.py --check=kernel --mutate=kappa
run gains                p2c_b8_boot.py --check=gains
run insens_gains_kappa   p2c_b8_boot.py --check=gains --mutate=kappa
run closure_planted      p2c_b8_boot.py --check=closure_planted
run run_L73.89_d0        p2c_b8_boot.py --L0=73.89 --json=$RAW/run_L73.89_d0.json
run run_L73.89_d1e7      p2c_b8_boot.py --L0=73.89 --d0=1e7 --json=$RAW/run_L73.89_d1e7.json
run run_L62_d1e7         p2c_b8_boot.py --L0=62 --d0=1e7 --json=$RAW/run_L62_d1e7.json
run K3_kappa0.02         p2c_b8_boot.py --L0=73.89 --kappa=0.02 --json=$RAW/K3_kappa0.02.json
run K4_tauD10            p2c_b8_boot.py --L0=62 --mutate=tauD10 --json=$RAW/K4_tauD10.json
run bisect_D_d0          p2c_b8_boot.py --bisect=56,62 --json=$RAW/bisect_D_d0.json
run bisect_D_d1e7        p2c_b8_boot.py --bisect=56,62 --d0=1e7 --json=$RAW/bisect_D_d1e7.json
run bisect_Dp_d0         p2c_b8_boot.py --bisect=54,62 --domain=Dprime --json=$RAW/bisect_Dp_d0.json
run bisect_Dp_d1e7       p2c_b8_boot.py --bisect=54,62 --d0=1e7 --domain=Dprime --json=$RAW/bisect_Dp_d1e7.json
echo "== done $(date -u '+%Y-%m-%d %H:%M')"
exit
}
