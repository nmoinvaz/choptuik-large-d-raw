#!/usr/bin/env python3
"""Old against new first-order files (#385): x, dx, omega, omega1, lam, lam1, lam1_sym, lam_mismatch.

    python compare_old_new.py OLD_DIR NEW_DIR [--out=comparison.md]

Per file, a table of both values and the relative difference |new - old| / |old| (components of the vectors x and dx
one by one). Reading fixed before the run: x, omega, omega1, lam and lam1 within 1e-6 relative are "reproduced"; a larger
difference there, and any change of lam1_sym or lam_mismatch beyond 1e-6, is a DISCREPANCY (reported, not fixed).
A nonzero difference of at most 1e-6 is shown as "differs" with its size.
"""
import json
import os
import sys

TOL = 1e-6
FILES = ["first_order_M1_xi0.2", "first_order_M3_xi0.2", "first_order_M3_xi0.175"]
SCALARS = ["omega", "omega1", "lam", "lam1", "lam1_sym", "lam_mismatch"]
VECTORS = ["x", "dx"]


def rel(new, old):
    return abs(new - old) / abs(old) if old != 0 else (0.0 if new == 0 else float("inf"))


def verdict(r, name):
    if r == 0:
        return "identical"
    if r <= TOL:
        return "differs"
    return "DISCREPANCY"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
    if len(args) != 2:
        sys.exit(__doc__)
    old_dir, new_dir = args
    lines = []
    ndisc = 0
    for stem in FILES:
        old = json.load(open(os.path.join(old_dir, stem + ".json")))
        new = json.load(open(os.path.join(new_dir, stem + ".json")))
        lines += [f"### {stem}.json", "", "| quantity | old | new | relative difference | reading |", "|---|---|---|---|---|"]
        for name in VECTORS:
            for i, (o, n) in enumerate(zip(old[name], new[name])):
                r = rel(n, o)
                v = verdict(r, name)
                ndisc += v == "DISCREPANCY"
                lines.append(f"| {name}[{i}] | {o:.15g} | {n:.15g} | {r:.2e} | {v} |")
        for name in SCALARS:
            if name not in old or name not in new:
                lines.append(f"| {name} | {old.get(name, 'absent')} | {new.get(name, 'absent')} | | absent |")
                continue
            r = rel(new[name], old[name])
            v = verdict(r, name)
            ndisc += v == "DISCREPANCY"
            lines.append(f"| {name} | {old[name]:.15g} | {new[name]:.15g} | {r:.2e} | {v} |")
        lines.append("")
    lines.append(f"{ndisc} entries differ by more than {TOL:g} relative (DISCREPANCY).")
    text = "\n".join(lines)
    print(text)
    if "--out" in opts:
        open(opts["--out"], "w", encoding="utf-8").write(text + "\n")


if __name__ == "__main__":
    main()
