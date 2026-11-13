# I599-mac: bit-identity checks of hp on multishoot's fallible preparation and public f64 projection, and of the multidouble 4.2.1 bump

Machine: the M5 Mac (a subagent of the coordinator). Tasks: https://github.com/nmoinvaz/choptuik-large-d/issues/599 and
https://github.com/nmoinvaz/choptuik-large-d/issues/614 (the multidouble bump, folded into the same branch).

Branch `wip/i599-subagent` of choptuik-large-d. The references are main's c3 build of this Mac (`I523-mac/c3`: hp/src
at 1658a4f on multishoot 1.2.1 and multidouble 4.1.0, fat LTO), T81's `ref_main.json` and `scaled_main.json`, and
`anm-mac/jets_inputs/jets_inputs.json` (the same hashes as c3's jets baseline). Each check's log ends in `exit N`.

- `checks/`: #599 alone, on multidouble 4.1.0. hp's two #599 commits built against the local multishoot branch
  `d1de161`, which is multishoot 1.2.2's code apart from two refusals of invalid input that no valid call reaches
  (low-memory recipe: `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `build.log`).
  `rust_tests.log` is hp's `cargo test --release --lib` on multishoot `f891639` (1.2.2's code).
- `checks_final/`: the branch's head `5ff29b6`, on multishoot 1.2.2 and multidouble 4.2.1 from crates.io (same recipe,
  strip off, `build2.log`), and `rust_tests.log` on it.
- `main_c3/`: `prepfail.py` on main's c3 build, the reference of `checks*/prepfail_vs_main.log`.
- `multishoot/`: multishoot's own `cargo test --release` logs (default, `mutate`, `portable`) of the merged PR's code.
- `run_checks.sh`, `run_checks2.sh` (adds `jets` and `jetsmut`): the sequences. `prepfail.py`: a state with a_h NaN
  makes the horizon LUs fail, and every entry point must raise the LU's error, with no panic message.

Controls: `bitsperturb` and `apiperturb` (one ulp of the first entry) must differ, `refmut` (a reference hash reversed)
must fail, `scaled` has its own (the scale wrong at order 7), `jetsmut` (`--mutate=kappa`) must fail, and `prepfail`'s
controls at the valid states must return values.
