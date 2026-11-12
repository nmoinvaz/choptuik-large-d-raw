# I600-win2: main's new kernel (hp on multishoot 1.2.1, the exact freeze projector) on Windows against the Mac's #523 references

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/600 (assigned by the coordinator at 14:10 UTC, 2026-11-12). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 8 threads of it, beside #594(b) and `hh_planted_tsign`.
Code: worktree `D:\choptuik-i600` detached at main `fc697f3a` (hp on multishoot 1.2.1; #523's 1658a4f and c2be1be are in it). Build: `build_hp.sh` (hp/build.sh with `VIRTUAL_ENV` and `PATH` set to a separate venv, `C:\Users\nathan\Source\venv-i600`: Python 3.14.10 and requirements.txt's pins, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0; multidouble was not installed in it before the build; rustc 1.96.0, cargo 1.96.0). `venv-t126`, which the running jobs use, was not touched. The build log is `build.log`.
References: the Mac's `I523-mac/c3/bits.json` and `api.json` (raw 44a0e702, with their perturb controls), `T81/ref_main.json`, `T81/scaled_main.json` and `anm-mac/jets_inputs/jets_inputs.json`, read from a worktree of origin/main of the raw repository (`D:/choptuik-large-d-raw-push`), since the live clone is not pulled. The checks are `run_600.sh` (modelled on `I523-mac/run_checks.sh`), each step writing `<step>.log` that ends `exit N`.
Pass (#600): every output of `xsolve_bits.py` and `api_bits.py` byte-identical to the Mac's c3, every perturb control differs, and the highm checks pass with `--mutate=kappa` failing. A difference between platforms is reported per entry point, not fixed. Results follow in this README.

## Results, fat-LTO build (venv-i600), 2026-11-12 16:41 to 16:53 UTC

**Build.** `build_hp.sh`, `build.log`: cargo `Finished release profile in 147m 27s`, exit 0 at 16:40:41 UTC (started 14:12:57; rustc 1.96.0, one core, 30.8 GB peak working set seen; the Mac's od-mac build took 31 min and 12.7 GB). `_hpkernel.cp314-win_amd64.pyd` sha256 4ede9afec7ffb40e93c321270ddc9614d644473e1b74834e9406a98f7571f90d. `hpkernel.isa()` and `multidouble.isa()` are both `avx2` (the Core Ultra 7 265K has no AVX-512); the Mac's build is NEON. numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0, Python 3.14.10, multishoot 1.2.1, multidouble 0.1.0 (the package at f092018d). A thin-LTO hedge (`build_hp_thin.sh`, `venv-i600b`, LTO off, 16 codegen units) was started at 15:30 and is not part of these results; its own section follows.

**The four pipelines** (`run_600.sh`, 2 threads each, started 16:41:00 UTC; references read from the worktree `D:/choptuik-large-d-raw-push` at 15628473: the c3 files are unchanged since the coordinator's 44a0e702):

| step | log | result | verdict |
|---|---|---|---|
| `xsolve_bits.py compare` against `I523-mac/c3/bits.json` | bits.log | **21 of 21 outputs byte-identical** | pass |
| `--perturb` dump against the win dump | bitsperturb.log | 0 of 21 identical (every output differs) | control fires, as it must |
| `api_bits.py compare` against `I523-mac/c3/api.json` | api.log | **175 of 176 identical; 1 differs: `jacobian_f64/mut1`** at the D 79.7657 state | the criterion (byte-identical) is not met by this one entry point, see below |
| `--perturb` dump against the win dump | apiperturb.log | 21 of 176 identical, 155 differ (the Mac's own apiperturb.log: 21 of 176) | control fires, as it must |
| `highm_check.py ref --compare=T81/ref_main.json --Ms=48,64,80` | ref.log | PASS: 72 outputs bit-identical | pass |
| `highm_check.py scaled --compare=T81/scaled_main.json` | scaled.log | PASS: 22 outputs bit-identical (M 192 and 256), its control (scale wrong at order 7) fires | pass |
| `highm_check.py jets --compare=anm-mac/jets_inputs/jets_inputs.json` | jets.log | PASS: 28 outputs bit-identical | pass |
| the same with `--mutate=kappa` | jetsmut.log | FAIL: 28 of 28 outputs differ | control fires, as it must |

**Extra check, not asked for.** The win perturb dumps compared with the Mac's own perturb dumps (`I523-mac/c3/bits_perturb.json`, `api_perturb.json`): bits 21 of 21 byte-identical (`bits_perturb_vs_mac_perturb.log`), api 175 of 176 with the same single entry `jacobian_f64/mut1` differing (`api_perturb_vs_mac_perturb.log`). So the 155 outputs that change under the perturbation change identically on both machines.

**The one difference, `jacobian_f64/mut1`** (`mut1_diag.py`, `mut1_diag.log`). `mutate=1` is the kernel's control "no tau derivative" (model.rs `dtau`), whose f64 Jacobian at the D 79.7657 state holds 45414 NaN and 21 inf entries out of 769 x 769. Three calls on this machine give the same bytes (so it is deterministic here). All NaN carry the bit pattern 0xFFF8000000000000, the sign-set default NaN of x86. With every NaN set to 0x7FF8000000000000 (arm64's default NaN) the hash is **277f42580c343c8ef896:(769, 769), exactly the Mac's stored hash**. So the two builds agree on every finite and infinite value and on the positions of the NaN; they differ only in the sign bit of the NaN that the hardware generates. `api_bits.py` hashes raw bytes, so it sees that. It is a platform difference of a mutation control's output, not of any value a solve uses; the other three mutation controls (`mut2`, `mut3`, `mut6`) and the unmutated `jacobian_f64` entries are byte-identical. Reported per entry point, not fixed (the pass criterion as written is not met by this one entry; the coordinator decides whether it counts).

**Reading.** A build on x86-64 (AVX2, MSVC target, Windows libm) gives the Mac's NEON build's bits for 21 of 21 `xsolve_bits` outputs, 175 of 176 api outputs (the 176th up to the NaN sign), and all 72 + 22 + 28 highm outputs at the stored resolutions, with every control firing.

## Results, thin build (venv-i600b), 2026-11-12 18:07 to 18:27 UTC

**Build.** `build_hp_thin.sh`, `build_thin.log`: the same commit fc697f3a in its own worktree `D:\choptuik-i600b`, `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6`, cargo `Finished release profile in 157m 13s`, exit 0 at 18:07:16 UTC (started 15:30; longer than the fat build's 147 min and with a similar 28.7 GB peak working set, so AGENTS.md's low-memory recipe lowered neither on this machine). `_hpkernel.cp314-win_amd64.pyd` sha256 b836d09e92baec73c00d1dcac2220579864b46fda49e7a9004dac09c35b053df (not the fat build's 4ede9afe...), `hpkernel.isa()` and `multidouble.isa()` both `avx2`, same pins as venv-i600.

**The eight steps** (`run_600.sh` with `PY`, `HP` and `OUT` set to this build, in `thin/`, two pipelines of 2 threads each, 18:07:37 to 18:26:40 UTC, with #603's chain and the #588 replicas running on the machine):

| step | thin build | fat build |
|---|---|---|
| bits against the Mac's c3 | 21 of 21 byte-identical | 21 of 21 |
| bits perturb control | 0 of 21 identical | 0 of 21 |
| api against the Mac's c3 | 175 of 176 (`jacobian_f64/mut1`, the NaN sign) | 175 of 176 |
| api perturb control | 21 of 176 identical | 21 of 176 |
| highm ref (48, 64, 80) | PASS, 72 bit-identical | PASS, 72 |
| highm scaled | PASS, 22 bit-identical, its control fires | PASS, 22 |
| highm jets | PASS, 28 bit-identical | PASS, 28 |
| jets `--mutate=kappa` | FAIL, 28 of 28 differ | FAIL, 28 of 28 |

**Fat against thin, bit for bit** (`thin/fat_vs_thin.log`, the dumps compared by `xsolve_bits.py compare` and `api_bits.py compare`): bits 21 of 21 byte-identical, bits perturb 21 of 21, **api 176 of 176**, api perturb 176 of 176. Both are x86, so the NaN sign of `jacobian_f64/mut1` agrees as well. So link-time optimisation and the codegen-unit count change no bit of any entry point checked here (the two binaries differ), and the thin build is a faster alternative only in that it needs no fat LTO; here it was not faster.

**Recommended tasks.** (1) `api_bits.py`'s digest could hash NaN as one pattern, so that a compare across ISAs ends 176 of 176; a one-line change in `digest` (not done here). (2) Done: the fat build against the thin one, see the thin section above (no bit differs).
