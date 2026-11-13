# I614-dh370: the x86 half of #614, hp on multishoot 1.2.2 and multidouble 4.2.1, built and checked on dh370 (Fedora Linux 45, AVX2)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/614
Code: choptuik-large-d main at 3c35f0cd0d7e8636eed426060f7f5e2a7824dad7, worktree `choptuik-large-d-614` with its own venv (no multidouble
installed before the build). The comparison build is I604-dh370/'s (main e835d94, worktree `choptuik-large-d-604`, the same kernel as
I523-mac/c3), left untouched. Toolchain: clang 23.1.5 as `cc`, `c++` and the cargo linker, rustc 1.99.1, maturin 1.16.0, Python 3.14.10.
No memory guard.

## Result

Every bit-identity check on the 3c35f0c build (multishoot 1.2.2, multidouble 4.2.1) equals both the Mac's c3 build and dh370's own #604 build (multishoot 1.2.1,
multidouble 4.1.0, the same kernel as c3), and each control fires. One chain step takes the same time on both builds, 3136 s on #604 and 3145 s on #614, and
the two saved states are byte-identical.

| check | 3c35f0c against Mac c3 / stored reference | against dh370 #604 | control |
|---|---|---|---|
| `cargo test --release --lib` | 24 passed, 2 ignored (the Mac's count), 712 s, peak 7851 MiB, exit 0 | | |
| `highm_check.py ref` M 48, 64, 80 (`ref.log`) | 72 of 72 identical to T81/ref_main.json | | |
| `highm_check.py scaled` (`scaled.log`) | PASS against T81/scaled_main.json | | its own control fires |
| `highm_check.py jets` (`jets.log`) | 28 of 28 identical to anm-mac/jets_inputs | | `--mutate=kappa`: 28 of 28 differ (`jets_mutate_kappa.log`) |
| `xsolve_bits.py` (`bits_vs_mac.log`, `bits_vs_604.log`) | 21 of 21 byte-identical | 21 of 21 | `--perturb`: 0 of 21 identical (`bitsperturb_control.log`) |
| `api_bits.py`, NaN as one pattern (`api_nan1_vs_*.log`) | 176 of 176 byte-identical | 176 of 176 | `--perturb`: 21 of 176 identical (`apiperturb_nan1_control.log`) |

`--perturb` dumps also compare identical to the Mac's and to #604's own perturbed dumps (`bitsperturb_vs_*.log`, `apiperturb_nan1_vs_*.log`). The NaN pattern is that
of I604-dh370: 45414 NaNs, all `0xFFF8000000000000`.

## One chain step on both builds

`timing614.sh`: #603's `anm_run.py` command with `--steps 1`, from `base/base_pin3_D225.1312.npz` (D 225.13125, M 32, pin 3, sha256 961d45ac2b3f3516758c...,
the file of I603-win2/base), 12 threads, `nice -n 10`, one build after the other, nothing else running. Both worktrees run the same Python driver (anm_run.py,
octo_corrector.py, hp/python, pinning.py and raw_out.py are identical between ff08351, where the #604 worktree stands, and 3c35f0c), so only hp/src/model.rs
and Cargo.toml, that is the kernel, differ. One run each, so no spread is known.

| | #604 build (multidouble 4.1.0) | #614 build (multidouble 4.2.1) | ratio |
|---|---|---|---|
| wall, `exit 0` | 3136 s | 3145 s | 1.003 |
| `t_coef`, the series coefficients (octo-double jets) | 2196.2 s | 2202.5 s | 1.003 |
| `t_corr`, the octo-double corrector, 5 steps | 709.1 s | 705.6 s | 0.995 |
| reseed | 83.12 s | 83.16 s | 1.000 |

`anm_pin3_D226.1312.npz` (sha256 8c3f620f774e8d01356b...) and `pred_pin3_D226.1312.npz` (sha256 9662f91ed641803ef48c...) are byte-identical between the two builds (`cmp`);
`cmp` of the new state against the base state differs at byte 15, so the comparison can fail. The two `anm_run.jsonl` records differ only in `t_coef` and `t_corr`.
The issue expected the x86 inlining to speed the octo-double chains, and here it does not, within one run each (0.3% slower, 0.5% faster for the corrector).

## Files

| file | what |
|---|---|
| `build614.sh`, `build.log` | `hp/build.sh` on 3c35f0c, exit 0, 2020 s, memory.peak 25113 MiB, no swap |
| `cargo_test614.sh`, `cargo_test.log` | Rust tests |
| `checks614.sh`, `checks_done.txt` | the five parallel check chains and their driver |
| `ref.log`, `scaled.log`, `jets.log`, `jets_mutate_kappa.log` | `highm_check.py` runs |
| `bits*.json`, `bits_*.log`, `bitsperturb_*.log` | `xsolve_bits.py` dumps and comparisons |
| `api_*.json`, `api_nan1_*.log`, `apiperturb_nan1_*.log` | `api_bits.py` dumps and comparisons (with `I604-dh370/api_bits_nan1.py`) |
| `timing614.sh`, `timing_b604.log`, `timing_b614.log`, `timing_done.txt` | the timed chain steps |
| `base/`, `chain_b604/`, `chain_b614/` | the start state and each build's outputs |
