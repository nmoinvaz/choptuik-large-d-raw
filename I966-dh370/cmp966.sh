#!/usr/bin/env bash
# #966 check 2: Delta of (d) with the options off against (d) (#961) and against #960's P1 state, with the control that the bound can fail.
# run from the raw clone's root: bash I966-dh370/cmp966.sh
PY=/home/nathan/Source/choptuik-large-d-961/.venv/bin/python
D=I961-dh370/step_n31/anm_pin3_D230.3408.npz; P=I960-dh370/n31/anm_pin3_D230.3408.npz; OFF=I966-dh370/step_n31_off/anm_pin3_D230.3408.npz
{ echo "== (d) options off against (d), bound 1e-40"; nice -n 10 $PY I961-dh370/delta_cmp961.py $D $OFF 1e-40; echo "exit $?"
  echo "== control, the same pair at bound 1e-60 (must be above)"; nice -n 10 $PY I961-dh370/delta_cmp961.py $D $OFF 1e-60 --expect-above; echo "exit $?"
  echo "== (d) options off against #960's P1 state, bound 1e-40"; nice -n 10 $PY I961-dh370/delta_cmp961.py $P $OFF 1e-40; echo "exit $?"
} > I966-dh370/delta_doff.log 2>&1
cat I966-dh370/delta_doff.log
