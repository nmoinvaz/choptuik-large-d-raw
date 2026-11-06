# anm-mac/md32: bit-identity checks of hp on multidouble 3.2.0 with split Cauchy sums (branch perf/md32, aeea2d1)

Machine: the Mac (Apple M5, NEON), the build of perf/md32 against the build of main at bfaa03d (venv-qds).

- `ref.log`: 168 of 168 outputs bit-identical to `anm-mac/md31/ref_old.json` (the old build's).
- `scaled.log`: PASS against `anm-mac/md31/scaled_old.json`.
- `jets.log`: 28 of 28 bit-identical against `anm-mac/jets_inputs/jets_inputs.json` (stored plans and inputs).
- `kappa.log`: the control, `--mutate=kappa`: 28 of 28 differ, exit 1.
