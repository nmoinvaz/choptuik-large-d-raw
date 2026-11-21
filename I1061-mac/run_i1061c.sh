#!/usr/bin/env bash
# P2 item 4 (#1061), third part: on D'_n (|x|^2 <= Z_B n) the closure did not depend on n0 down to e^54; find where
# it stops. Below ln n = 10.8 the far region F is empty (sqrt(Z_B n) < x_F), so the brackets start at 11.
{
set -u
PY=/Users/nathan/venv-314/bin/python
run() { local name=$1; shift; echo "== $name: $* ($(date -u '+%Y-%m-%d %H:%M'))"; nice -n 10 $PY "$@" > "$RAW/$name.log" 2>&1; echo "   exit $?"; tail -2 "$RAW/$name.log"; }
run bisect_Dp_d0_low     p2c_b8_boot.py --bisect=11,54 --domain=Dprime --tol=0.5 --json=$RAW/bisect_Dp_d0_low.json
run bisect_Dp_d1e7_low   p2c_b8_boot.py --bisect=11,56 --d0=1e7 --domain=Dprime --tol=0.5 --json=$RAW/bisect_Dp_d1e7_low.json
echo "== done $(date -u '+%Y-%m-%d %H:%M')"
exit
}
