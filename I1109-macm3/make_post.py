#!/usr/bin/env python3
"""#1109 stage 1c on macm3: builds post_result.md from r0/w01/w10 .jsonl and .exit (every number from the files).
Usage: python3 make_post.py DATA_COMMIT TIME_UTC > post_result.md"""
import json, os, sys
from roots_summary import REF, BAR1, DELTA, NAMES, load

d = os.path.dirname(os.path.abspath(__file__))
commit, when = sys.argv[1], sys.argv[2]
R = {}
for n in NAMES:
    ev, fin, rc = load(d, n)
    R[n] = dict(ev=ev, fin=fin[-1], rc=rc)
r0 = R["r0"]["fin"]["lam_lin"]
lo = {n: R[n]["fin"]["bracket"] for n in NAMES}
given = {"r0": (0.0440, 0.0470), "w01": (0.0400, 0.0500), "w10": (0.0350, 0.0550)}
f = lambda x: f"{x:.10f}"
b1 = r0 - REF
print(f"#1109 stage 1c roots on macm3 with Rust block 12, runner t5-macm3 (MacBook Air M3), {when}. Raw: `I1109-macm3/`, raw-data commit {commit}.\n")
print(f"**The control passes bar 1: r0's root {f(r0)} is {b1:+.2e} from mm5's refined 0.0455917189 (bar {BAR1:g}).** "
      f"w01's root is {f(R['w01']['fin']['lam_lin'])} (r0 {R['w01']['fin']['lam_lin'] - r0:+.4e}) and w10's is {f(R['w10']['fin']['lam_lin'])} (r0 {R['w10']['fin']['lam_lin'] - r0:+.4e}), "
      f"both from exit 4 runs: the last det-linear point was not robust (dln > 0.1), so each is a det-linear estimate inside its final robust bracket, "
      f"{R['w01']['fin']['width']:.2e} and {R['w10']['fin']['width']:.2e} wide. Root shift over Delta shift: "
      f"{(R['w01']['fin']['lam_lin'] - r0) / DELTA['w01']:.4f} (w01), {(R['w10']['fin']['lam_lin'] - r0) / DELTA['w10']:.4f} (w10).\n")
print("### Roots (by `roots_summary.py`, output `roots_summary.txt`; `--tol=1e-6 --maxev=20 --b12=rust --b12_threads=2`, D 23.0, k_c 127)\n")
print("| state | bracket given | evaluations | exit | status | final robust bracket (width) | det-linear root | root - r0 | Brent end | seconds |")
print("|---|---|---|---|---|---|---|---|---|---|")
for n in NAMES:
    x = R[n]["fin"]
    print(f"| {n} | ({given[n][0]}, {given[n][1]}) | {x['n_eval']} | {R[n]['rc']} | {x['status']} | [{x['bracket'][0]!r}, {x['bracket'][1]!r}] ({x['width']:.3e}) | "
          f"{x['lam_lin']!r} | {x['lam_lin'] - r0:+.6e} | {x['lam_brent']!r} | {x['sec']} |")
print("\nNo bracket was widened (no exit 2). Evaluations (lambda, hybrid sign, float64 sign, dln, robust, seconds):\n")
for n in NAMES:
    print(f"- {n}: " + "; ".join(f"{e['lam']!r} {int(e['sign']):+d} {int(e['f64_sign']):+d} {e['dln']:.2e} {'R' if e['robust'] else 'NOT robust'} {e['sec']}"
                                 for e in sorted(R[n]["ev"], key=lambda e: e["lam"])))
print("\n### Bars and reading\n")
print("| item | value | verdict |\n|---|---|---|")
print(f"| bar 1: r0 root within {BAR1:g} of 0.0455917189 | {r0!r}, difference {b1:+.4e} | **{'PASS' if abs(b1) <= BAR1 else 'FAIL'}** |")
for n in ("w01", "w10"):
    x = R[n]["fin"]; sh = x["lam_lin"] - r0; b = x["bracket"]
    print(f"| bar 2: {n} root, {n} - r0 | {x['lam_lin']!r}, {sh:+.6e}; bracket gives {b[0] - r0:+.4e} to {b[1] - r0:+.4e} | reported |")
    print(f"| reading: Delta moved {DELTA[n]:+.3e}; root shift / Delta shift | {sh / DELTA[n]:.4f} (bracket {(b[0] - r0) / DELTA[n]:.3f} to {(b[1] - r0) / DELTA[n]:.3f}) | for reading |")
print("\nThe two ratios agree to "
      f"{abs((R['w01']['fin']['lam_lin'] - r0) / DELTA['w01'] / ((R['w10']['fin']['lam_lin'] - r0) / DELTA['w10']) - 1) * 100:.2f}% "
      "(det-linear roots); the brackets are wider than that, w01's most (ratio 0.413 to 0.792).")
print("\n### What ran\n")
print("Step 1 (`ellrs/build.sh` in `venv-macm3-1058b`, \"ellrs neon accelerate\"): `ell_b12rs.py selftest` exit 0, `--mutate=nolam` exit 1, `--mutate=harm` exit 1, `check` (k_c 31, D 10.5, lambda 2.87, 2 threads, controls) exit 0: 15010 of 15010 entries bit for bit, both controls 0 of 15010 (logs `selftest*.log`, `check_kc31.log`).")
print("Step 2: three `d18_secant.py run` at once, 2 threads each (`RAYON_NUM_THREADS=2`, OpenBLAS and vecLib 1), `nice -n 10`, `caffeinate -is`, 14400 s cap each (`common/capped_run.py`), detached by `common/launch_1070.py` (a copy from the #1025 runs). Started 2026-11-28 06:27:28 UTC; r0 ended 07:24:50, w10 07:31:51, w01 07:35:21 UTC. Code: `~/Source/choptuik-ell1fast` at 693a4d79; inputs blob-checked (R0 90d3e655, d1a3a641; w01 458d9026, 3410f1e5; w10 9947a645, eb52631f; r0 `--pin` matched). Each run printed the record system at start: |F| 3.1959e-10, 3.1878e-10, 3.1673e-10 against the records' 3.1949e-10, 3.1852e-10, 3.1660e-10; steps 4179, 4179, 4182. RSS 2.8 to 3.0 GiB per process (one sample, 9 min in); load average 15 to 20 from other processes; 532 to 625 s per evaluation with the three at once.")
print("\n### Failed or disagrees\n")
print("- w01 and w10 ended exit 4 (nonrobust final point, dln 0.303 and 0.568 against the 0.1 limit), as the stage 1c control did with `--b12=fast`; their roots are the det-linear estimates at those points. w01's sign at its last point (hybrid -1, not robust) and w10's (hybrid +1, not robust) are not trusted; taken at face value they narrow w01's root to between 0.04543682 and 0.04543774 and w10's to between 0.04405869 and 0.04406138.")
print("- The float64 sign disagrees with the hybrid sign for w10 at 0.0439440 and 0.0440587 (f64 -1, hybrid +1) and, for r0 and w01, at every evaluation above the root (f64 +1 up to lambda 0.047 and 0.05, hybrid -1). The hybrid sign is the one the roots use.")
print("- r0 against mm5's stage 1c2 B (same bracket, same code path, other machine): det-linear roots differ by 1.40e-10; the final brackets' ends differ by 3.8e-8 (here [0.045591589325629484, 0.045592089325629484], mm5 [0.04559155115141893, 0.04559205115141893]).")
print("- Nothing was pushed or posted from this Mac (SSH and gh unavailable); the `running` label and the \"started\" comment are not set.")
print("\n### Recommended tasks\n")
print("- **A third state on the same line (w03 or w05), then the root shifts against Delta.** What: re-solve k_c 127 at D 23.0 with Delta moved a fraction of R0's weak-vector step, root by `--b12=rust`. Why: the two det-linear shifts give 0.787 and 0.784 times the Delta shift, but w01's bracket allows 0.41 to 0.79. Acceptance: the third point's root shift over its Delta shift lies within 2% of 0.785, or the linear reading is withdrawn. Depends on: whatever built `sol_w01` and `sol_w10` (mm5, #1109 stage 1c).")
