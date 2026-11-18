# I958-dh170: hp on multidouble 4.9.0 and multishoot 3.3.0 (branch deps/multidouble-4.9.0), same bits as 4.8.2 and 3.2.0?

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/958
(body, amendment IC_kwDOVPE7OM8AAAABn3U8bw of 05:42 UTC and the second amendment IC_kwDOVPE7OM8AAAABn6rfPA of 08:54 UTC, which assigns it to dh170).

## Setup

- **Build D**: worktree `~/Source/choptuik-large-d-958`, detached at origin/deps/multidouble-4.9.0 = **5b7cef1b** (hp: multidouble 4.9.0 and
  multishoot 3.3.0; carries main's `jet_by_order_check.py` 9bff3a1e and the `modecount_cx` fix), fresh uv venv `.venv` (SETUP.md steps,
  `uv venv --seed --python 3.14`, `uv pip install -r requirements.txt`), `hp/build.sh` with the low-memory recipe
  (`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=10`, nice 15) under `/usr/bin/time -v`
  (`build958.sh`, `build.log`). `versions_D.txt`: `hpkernel.__file__`, the crate versions of `hp/Cargo.lock` and the strings of the .so.
- **Build A (the reference)**: dh170's own 4.8.2 build, `~/Source/choptuik-large-d-935/.venv` (hpkernel built 2026-11-17 for #935 from
  branch hp/multidouble-4.8.2 cdb5a6bc; multidouble 4.8.2 / multishoot 3.2.0 / multisolver 0.1.1). Its crate versions are recorded in
  `versions_A.txt` from its .so. `octo_hashes.py` is run from the same `hp/` (build D's worktree) with each venv's python, so the script and the
  Python modules it imports are the same bytes and only the compiled kernel and the multidouble Python package differ.
- **Inputs**, read-only, extracted from the raw repository's origin/main (`raw_commit.txt`, byte for byte, no pull in the live clone) into
  `~/scratch958/raw` = R: ST = `I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz`, ST2 = `I608-dh610/restart4_d6/anm_pin3_D253.3382.npz`,
  `T81/ref_main.json`, `T81/scaled_main.json`, `anm-mac/jets_inputs/jets_inputs.json` (and its inputs npz), `I954-dh610/` (build A on dh610 for #954).
- Checks at `--threads 6` from build D's `hp/`, nice 10, one after another (`checks958.sh`), 2 threads left for #949's intake.

## Checks and pass criteria, written before the build

| # | check | pass |
|---|---|---|
| 1a | `highm_check.py ref --compare=R/T81/ref_main.json --Ms=48,64,80` | exit 0, 72/72 bit-identical |
| 1b | `highm_check.py scaled --compare=R/T81/scaled_main.json` | exit 0, 22/22 |
| 1c | `highm_check.py jets --compare=R/anm-mac/jets_inputs/jets_inputs.json` | exit 0, 28/28 |
| 1d | the same with `--mutate=kappa` | exit 1, 28/28 differ (the control fires) |
| 2 | `octo_hashes.py R ST --threads 6 --N 6` and the same at ST2, on build D and on build A, diffed | every line equal, or each differing line located to its operation and sized |
| 2c | `--mutate_dz 1` on build D at ST | differs from the unmutated output only on its own line |
| 3a | `jet_by_order_check.py R ST --threads 6 --N 6` (main's script, 9bff3a1e) | exit 0 |
| 3b | `jac_tangents_check.py R ST --threads 6` | exit 0 |

A difference is a result, not a failure: it is located to its operation (residual, Jacobian with one or two tangents, the Newton step and its
pivots, or the order of the series, the first differing entry of each part) and reported with its size. Decision it informs: whether
the multidouble 4.9.0 bump can use the stored references.
