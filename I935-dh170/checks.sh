#!/bin/bash
# #935 on dh170: the reference checks of AGENTS.md against the new venv (multidouble 4.8.2). Exits 0 only when ref, scaled
# and jets exit 0 and jets --mutate=kappa exits non-zero. Each log is ref.log, scaled.log, jets.log, jets_kappa.log.
W=$HOME/Source/choptuik-large-d-935
RAW=$HOME/Source/choptuik-large-d-raw
OUT=$RAW/I935-dh170
P=$W/.venv/bin/python
cd "$W/hp" || exit 1
L=$OUT/checks.log
echo "# $(date -u '+%F %T') UTC, $(git -C "$W" rev-parse --short HEAD), raw $(git -C "$RAW" rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L"
run() { n=$1; shift; echo "== $n $(date -u '+%H:%M:%S')" >> "$L"; nice -n 10 "$@" > "$OUT/$n.log" 2>&1; rc=$?; echo "$n exit $rc $(date -u '+%H:%M:%S')" >> "$L"; return $rc; }
run ref $P highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80; A=$?
run scaled $P highm_check.py scaled --compare=$RAW/T81/scaled_main.json; B=$?
run jets $P highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json; C=$?
run jets_kappa $P highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa; D=$?
RC=0; [ $A = 0 ] && [ $B = 0 ] && [ $C = 0 ] && [ $D != 0 ] || RC=1
echo "# $(date -u '+%F %T') UTC, ref $A, scaled $B, jets $C, jets kappa $D (must be non-zero)" >> "$L"
echo "exit $RC" >> "$L"
exit $RC
