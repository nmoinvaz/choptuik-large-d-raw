Command list extracted (2026-11-22 03:33 UTC), saved before any run.

- **108 rows** from README.md at d7d54ccf: 21 quote an invocation (arguments, a `cd`, or a fenced line) and 87 name a script as the source of a number or figure.
- **41 rows quote numbers** (203 numbers), each read from the README at run time by a locator, so a changed number in a copy of the README changes the expectation.
- 10 rows are marked not run before the pass: `pip install .`, `cargo test --release`, `./build.sh main`, `hp/build.sh` (no builds), `fixed_point.py`, `fixed_point_M.py`, `validated_int.py`, `krawczyk.py` (named as code, no invocation or number quoted), `amp_flint.py`, and `hp/states.py` (a module).
- The coverage check finds no code span of the README that looks like a command and is no row. 139 file names in code spans: 138 exist; `_J1000_phys.json` (line 1595) is an abbreviation.
- Script `reproduce_readme.py` on branch `wip/i349-reproduction` (8a0c35b1). Next: the control, then pass 1 in the clean venv (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0), then pass 2 with an existing build.
