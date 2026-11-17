#!/bin/bash
# #935 on dh370: the reference checks of the multidouble 4.8.2 build (worktree choptuik-large-d-935, its .venv). ref,
# scaled and jets run side by side, one thread each, nice 10; the jets kappa control follows jets. References are T81
# and anm-mac of the raw clone. Exits non-zero when a check that must pass fails or the control that must fail passes.
WT=/home/nathan/Source/choptuik-large-d-935
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I935-dh370
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa(), hpkernel.__file__)" > "$OUT/isa.log" 2>&1
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%F %H:%M:%S') $(git -C "$WT" rev-parse --short HEAD) $*" > "$OUT/$name.log"
  nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
  echo "exit $?" >> "$OUT/$name.log"
}
chain_ref()    { run ref python highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80; }
chain_scaled() { run scaled python highm_check.py scaled --compare=$RAW/T81/scaled_main.json; }
chain_jets()   { J=$RAW/anm-mac/jets_inputs/jets_inputs.json
                 run jets python highm_check.py jets --compare=$J
                 run jets_mutate_kappa python highm_check.py jets --compare=$J --mutate=kappa; }
chain_ref & chain_scaled & chain_jets &
wait
rc() { tail -1 "$OUT/$1.log" | sed 's/exit //'; }
bad=0
for n in ref scaled jets; do
  [ "$(rc $n)" = 0 ] || { echo "MUST PASS failed: $n (exit $(rc $n))" >> "$OUT/exits_935.txt"; bad=1; }
done
[ "$(rc jets_mutate_kappa)" != 0 ] || { echo "CONTROL passed: jets_mutate_kappa" >> "$OUT/exits_935.txt"; bad=1; }
echo "checks done $(date -u '+%F %T'), ref $(rc ref), scaled $(rc scaled), jets $(rc jets), jets kappa $(rc jets_mutate_kappa), verdict exit $bad" >> "$OUT/exits_935.txt"
exit $bad
