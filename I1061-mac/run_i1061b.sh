#!/usr/bin/env bash
# P2 item 4 (#1061), second part: the steps after run_L62_d1e7 of run_i1061.sh, with the offset brackets corrected.
{
set -u
PY=/Users/nathan/venv-314/bin/python
run() { local name=$1; shift; echo "== $name: $* ($(date -u '+%Y-%m-%d %H:%M'))"; nice -n 10 $PY "$@" > "$RAW/$name.log" 2>&1; echo "   exit $?"; tail -2 "$RAW/$name.log"; }
run run_L62_d0           p2c_b8_boot.py --L0=62 --json=$RAW/run_L62_d0.json
run K3_kappa0.02         p2c_b8_boot.py --L0=73.89 --kappa=0.02 --json=$RAW/K3_kappa0.02.json
run K4_tauD10            p2c_b8_boot.py --L0=62 --mutate=tauD10 --json=$RAW/K4_tauD10.json
run bisect_D_d0          p2c_b8_boot.py --bisect=56,62 --json=$RAW/bisect_D_d0.json
run bisect_D_d1e7        p2c_b8_boot.py --bisect=62,74 --d0=1e7 --json=$RAW/bisect_D_d1e7.json
run bisect_Dp_d0         p2c_b8_boot.py --bisect=54,62 --domain=Dprime --json=$RAW/bisect_Dp_d0.json
run bisect_Dp_d1e7       p2c_b8_boot.py --bisect=56,74 --d0=1e7 --domain=Dprime --json=$RAW/bisect_Dp_d1e7.json
run fine_L62_d0          p2c_b8_boot.py --L0=62 --n1c=320 --n0c=48 --json=$RAW/fine_L62_d0.json
run fine_L73.89_d1e7     p2c_b8_boot.py --L0=73.89 --d0=1e7 --n1c=320 --n0c=48 --json=$RAW/fine_L73.89_d1e7.json
echo "== done $(date -u '+%Y-%m-%d %H:%M')"
exit
}
