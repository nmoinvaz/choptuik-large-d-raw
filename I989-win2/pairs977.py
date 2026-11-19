"""#977: every pairwise distance among zeros with their error estimates.

    python pairs977.py ZEROS.json            [{"name": ..., "A": ..., "w": ..., "est": ...}, ...]
    python pairs977.py --selftest [--mutate=norm|swap]

For a pair (i, j) the distance is the Euclidean norm of the difference in (A, w/w_inf), given in units of est_i, of est_j and of
est_i + est_j (the combined estimate). `within sum` is distance <= est_i + est_j.
"""
import json, sys
import numpy as np


def pairs(zs, mut=""):
    out = []
    for i in range(len(zs)):
        for j in range(i + 1, len(zs)):
            a, b = zs[i], zs[j]
            d = np.array([a["A"] - b["A"], a["w"] - b["w"]])
            dist = float(np.abs(d).sum() if mut == "norm" else np.hypot(*d))
            ei, ej = (b["est"], a["est"]) if mut == "swap" else (a["est"], b["est"])
            out.append((a["name"], b["name"], d[0], d[1], dist, dist / ei, dist / ej, dist / (a["est"] + b["est"]),
                        dist <= a["est"] + b["est"]))
    return out


def show(rows):
    print("| zero i | zero j | dA | dw | distance | in est i | in est j | in est i + est j | within the sum |")
    print("|---|---|---|---|---|---|---|---|---|")
    for n1, n2, dA, dw, dist, ui, uj, us, w in rows:
        print(f"| {n1} | {n2} | {dA:+.2e} | {dw:+.2e} | {dist:.2e} | {ui:.2f} | {uj:.2f} | {us:.2f} | {'yes' if w else 'no'} |")


def selftest(mut):
    zs = [{"name": "p", "A": 0.0, "w": 0.0, "est": 1.0}, {"name": "q", "A": 3.0, "w": 4.0, "est": 2.0}]
    (_, _, dA, dw, dist, ui, uj, us, w), = pairs(zs, mut)
    ok = abs(dist - 5) < 1e-12 and abs(ui - 5 / 1.0) < 1e-12 and abs(uj - 5 / 2.0) < 1e-12 and abs(us - 5 / 3.0) < 1e-12 and not w
    print(f"planted (0,0 est 1) and (3,4 est 2): distance {dist}, units {ui:.3f} {uj:.3f} {us:.3f}, within sum {w}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        m = [t.split("=")[1] for t in sys.argv if t.startswith("--mutate=")]
        sys.exit(selftest(m[0] if m else ""))
    show(pairs(json.load(open(sys.argv[1]))))
