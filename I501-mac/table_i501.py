#!/usr/bin/env python3
"""Markdown tables of near_null's first Newton step from its jsons (#501): a summary row per run and step, and the
split by block of each step, the runs side by side.

    python3 table_i501.py RUN=FILE.json ...    (RUN a column name, e.g. 0.7=near_null_planted.json)
"""
import json
import sys


def main():
    runs = [a.split("=", 1) for a in sys.argv[1:]]
    recs = [(n, json.load(open(f))) for n, f in runs]
    print("| run | step | plan | max\\|dz\\| | \\|dz\\| | Delta | share on span(V) | V^T dz (v_1..v_k) |")
    print("|---|---|---|---|---|---|---|---|")
    for n, r in recs:
        for key in ("step", "step_pinned"):
            s = r[key]
            vt = ", ".join(f"{x:+.2e}" for x in s["vt"])
            print(f"| {n} | {key} | {r['plan']} | {s['max']:.3e} | {s['norm']:.3e} | {s['delta']:+.3e} | {s['share']:.4f} | {vt} |")
    for key in ("step", "step_pinned"):
        print()
        print(f"{key}: per block, norm (largest harmonic, its amplitude)")
        print()
        print("| block | " + " | ".join(n for n, _ in recs) + " |")
        print("|---|" + "---|" * len(recs))
        names = []
        for _, r in recs:
            for b in r[key]["blocks"]:
                if b not in names:
                    names.append(b)
        for b in names:
            cells = []
            for _, r in recs:
                x = r[key]["blocks"].get(b)
                if x is None:
                    cells.append("")
                else:
                    h, a = x["top"][0]
                    cells.append(f"{x['norm']:.2e} (k{h} {a:.1e})")
            print(f"| {b} | " + " | ".join(cells) + " |")
        print("| Delta | " + " | ".join(f"{r[key]['delta']:+.2e}" for _, r in recs) + " |")


if __name__ == "__main__":
    main()
