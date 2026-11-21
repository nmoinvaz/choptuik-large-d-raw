#!/usr/bin/env python3
"""#1025 D 18 upper root, k_c 63: the gate before the dd check. P4 rules and the outer-grid-point edge rule by raw I1025-mac/d18/d18_check.py (run as a subprocess), plus the bracket check
fixed before the run: the root lies in the scan's bracket (1.800, 1.810), so it is the upper root and not the lower one (1.7749781).
usage: d18_gate.py HYBRID.jsonl D18_CHECK.py PYTHON   |   d18_gate.py selftest PYTHON D18_CHECK.py"""
import json, os, subprocess, sys, tempfile
LO, HI = 1.800, 1.810


def gate(js, chk, py):
    r = [json.loads(l) for l in open(js) if l.strip() and abs(json.loads(l)["D"] - 18.0) < 1e-9][-1]
    p = subprocess.run([py, chk, js, "18.0"], capture_output=True, text=True)
    rules = p.returncode == 0
    lam = r["lam"]
    inb = lam is not None and LO < lam < HI
    return rules, inb, p.stdout.rstrip(), r


if sys.argv[1] == "selftest":
    py, chk = sys.argv[2], sys.argv[3]
    d = tempfile.mkdtemp(prefix="d18gate_")
    g = 1.825
    w = 0.02

    def rec(root, signs, nall=1, nch=1, robust=True, bw=2e-8, system=True):
        grid = [g * (1 - w), g, g * (1 + w)]
        return dict(D=18.0, kc=63, mode="hybrid", lam=root, lam_guess=g, evals={repr(l): dict(sign=s) for l, s in zip(grid, signs)}, record_system=system,
                    n_signchanges_grid=nch, n_changes_all=nall, noise_robust=robust, bracket_width=bw)
    cases = [("upper root, + - -", rec(1.8063, [1, -1, -1]), True),
             ("lower root 1.7750 (not in the bracket)", rec(1.7750, [-1, 1, 1]), False),
             ("root 1.8063 but two grid changes", rec(1.8063, [-1, 1, -1], nch=2, nall=2), False),
             ("root 1.8063 not noise-robust", rec(1.8063, [1, -1, -1], robust=False), False),
             ("root 1.8063 not the record system", rec(1.8063, [1, -1, -1], system=False), False),
             ("root 1.8063, bracket 1e-6", rec(1.8063, [1, -1, -1], bw=1e-6), False),
             ("root 1.7900 (inside the window, outside the scan bracket)", rec(1.7900, [1, -1, -1]), False),
             ("root 0.03 steps from the outer lower point (1.7895)", rec(1.7895, [1, -1, -1]), False)]
    bad = 0
    for i, (name, r, want) in enumerate(cases):
        f = os.path.join(d, f"c{i}.jsonl")
        open(f, "w").write(json.dumps(r) + "\n")
        rules, inb, _, _ = gate(f, chk, py)
        got = rules and inb
        bad += got != want
        print(f"selftest {name}: rules {'pass' if rules else 'FAIL'}, bracket {'pass' if inb else 'FAIL'} -> {'PASS' if got else 'FAIL'} (want {'PASS' if want else 'FAIL'}) {'ok' if got == want else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)")
    sys.exit(1 if bad else 0)
rules, inb, out, r = gate(sys.argv[1], sys.argv[2], sys.argv[3])
print(out)
print(f"bracket check: root {r['lam']!r} in ({LO}, {HI}): {'pass' if inb else 'FAIL'}")
print(f"GATE D 18.0 k_c 63: {'PASS' if rules and inb else 'FAIL'} (P4 rules and outer-edge rule {'pass' if rules else 'FAIL'}, bracket {'pass' if inb else 'FAIL'}) lam {r['lam']!r}")
sys.exit(0 if rules and inb else 1)
