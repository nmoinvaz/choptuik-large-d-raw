"""#1025, the coordinator's check of det's sign convention across the k_c 63 states (d18_criteria.log): the hybrid sign at two
reference lambdas on each state, compared between consecutive states in D order. Both constant: the convention holds and
orientations compare. Both flip between two states: a global flip there, orientations compare only within one state. One flips:
a root crossed that reference, the coordinator rules. A reference point that is not noise-robust is not counted.
usage: d18_refsign_read.py REFS.jsonl [--refs=1.2,2.6]   |   d18_refsign_read.py selftest [--mutate=ends]"""
import sys, json
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
REFS = next((tuple(float(v) for v in a.split("=", 1)[1].split(",")) for a in sys.argv if a.startswith("--refs=")), (1.2, 2.6))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sg = lambda s: "+" if s > 0 else "-"


def read(rows, refs=REFS, out=print):
    by = {}
    for r in rows:
        by.setdefault(r["D"], {})[round(r["lam"], 6)] = r
    Ds = sorted(by)
    miss = [(D, x) for D in Ds for x in refs if round(x, 6) not in by[D]]
    if miss:
        out(f"missing reference points: {miss}; no reading")
        return dict(v="incomplete", pairs=[])
    for D in Ds:
        out(f"D {D:g}: " + "; ".join(f"{x:.2f} hybrid {sg(by[D][x]['sign'])}{'' if by[D][x]['noise_robust'] else ' (NOT noise-robust)'} "
                                    f"ln|det| {by[D][x]['ln']:.4f}, float64 {sg(by[D][x]['f64_sign'])}" for x in refs)
            + f" ({by[D][refs[0]]['state']})")
    seq = [Ds[0], Ds[-1]] if MUT == "ends" else Ds                # control: only the first and last state compared
    pairs = []
    for a, b in zip(seq, seq[1:]):
        rob = all(by[D][x]["noise_robust"] for D in (a, b) for x in refs)
        fl = [x for x in refs if by[a][x]["sign"] != by[b][x]["sign"]]
        k = "unresolved" if not rob else "none" if not fl else "global flip" if len(fl) == len(refs) else f"{fl[0]:.2f} only"
        pairs.append((a, b, k))
        out(f"  D {a:g} -> {b:g}: {k}")
    ks = [k for _, _, k in pairs]
    if all(k == "none" for k in ks):
        v = "holds"
        out("reading: both reference signs are constant across D; the convention holds and orientations compare across D")
    elif "unresolved" in ks:
        v = "unresolved"
        out(f"no reading: a reference point is not noise-robust at {[(a, b) for a, b, k in pairs if k == 'unresolved']}; the coordinator rules")
    elif any(k.endswith("only") for k in ks):
        v = "one reference"
        out(f"no convention reading: one reference flips alone at {[(a, b, k) for a, b, k in pairs if k.endswith('only')]} (a root crossed it); "
            f"global flips at {[(a, b) for a, b, k in pairs if k == 'global flip'] or 'none'}; the coordinator rules")
    else:
        v = "global flip"
        out(f"reading: a global flip between {[(a, b) for a, b, k in pairs if k == 'global flip']}; orientations compare only within one state")
    return dict(v=v, pairs=pairs)


def planted(Ds, s12, s26, nonrob=()):
    return [dict(D=D, lam=x, sign=float(s), ln=-1900.0, f64_sign=float(s), noise_robust=(D, x) not in nonrob, state=f"planted_D{D:g}")
            for D, a, b in zip(Ds, s12, s26) for x, s in ((1.2, a), (2.6, b))]


def selftest():
    Ds = [17.75, 18.0, 18.0625, 18.125, 18.1875, 18.25, 18.5]
    q = lambda *a: None
    cases = [
        ("constant signs: holds", planted(Ds, [-1] * 7, [1] * 7), "holds"),
        ("a flip at both and back (D 18.1875 alone flipped): two global flips",
         planted(Ds, [-1, -1, -1, -1, 1, -1, -1], [1, 1, 1, 1, -1, 1, 1]), "global flip"),
        ("2.60 alone flips between D 18.25 and 18.5: one reference", planted(Ds, [-1] * 7, [1] * 6 + [-1]), "one reference"),
        ("a non-robust 1.20 at D 18.0625: unresolved", planted(Ds, [-1] * 7, [1] * 7, nonrob=((18.0625, 1.2),)), "unresolved"),
        ("a missing point: incomplete", planted(Ds, [-1] * 7, [1] * 7)[:-1], "incomplete"),
    ]
    ok = []
    for name, rows, want in cases:
        r = read(rows, (1.2, 2.6), q)
        good = r["v"] == want and (want != "global flip" or [(a, b) for a, b, k in r["pairs"] if k == "global flip"] == [(18.125, 18.1875), (18.1875, 18.25)])
        ok.append(good); print(f"planted: {name}: {'PASS' if good else 'FAIL'} (read {r['v']})")
    print(f"selftest: {'PASS' if all(ok) else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    rows = [json.loads(l) for l in open(args[0])]
    print(f"{args[0].rsplit('/', 1)[-1]}: {len(rows)} records, references {REFS}")
    read(rows)
