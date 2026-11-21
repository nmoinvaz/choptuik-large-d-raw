"""#1025, beside the sign-convention check (d18_criteria.log): per consecutive pair of states, the reference flips (d18_refsign_read.py,
unchanged) beside the frozen RK4 step-count changes (dss_ell.freeze_from with the record's kappa), inner segments first ('log' and the
segments ending at or below x 0.16), every changed segment beside them; whether each flip lines up with an inner change; and the
coordinator's ruling on a one-reference flip: a root crossed that reference, orientations compare from the side whose reference held.
usage: d18_refsign_steps.py REFS.jsonl REC.jsonl:STATE.npy:D,...   |   d18_refsign_steps.py selftest [--mutate=shift]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, HERE)
import d18_refsign_read as rr

inner = lambda k: k == "log" or (isinstance(k, tuple) and max(k) <= 0.16 + 1e-12)
seg = lambda k: k if k == "log" else f"{k[0]:g}-{k[1]:g}"


def table(rows, steps, out=print, refs=(1.2, 2.6)):
    r = rr.read(rows, refs, out=lambda *a: None)
    Ds = sorted(steps)
    ch = {}
    for a, b in zip(Ds, Ds[1:]):
        ch[(a, b)] = {k: (steps[a][k], steps[b][k]) for k in steps[b] if steps[a].get(k) != steps[b][k]}
    keys = list(ch)
    if MUT == "shift":                                        # control: each pair is given the next pair's step changes
        ch = {keys[i]: ch[keys[(i + 1) % len(keys)]] for i in range(len(keys))}
    res = []
    for a, b, k in r["pairs"]:
        c = ch[(a, b)]
        ci = {seg(s): v for s, v in c.items() if inner(s)}
        co = [seg(s) for s in c if not inner(s)]
        line = f"D {a:g} -> {b:g}: {k}; inner segments changed {ci or 'none'}; others changed {len(co)} ({', '.join(co) or 'none'})"
        if k.endswith("only"):
            x = float(k.split()[0]); held = [y for y in refs if abs(y - x) > 1e-9][0]
            line += f"; ruling: a root crossed {x:.2f}, orientations compare from the {held:.2f} side (roots counted from {held:.2f})"
        out(line)
        res.append((a, b, k, bool(ci)))
    fl = [(a, b, i) for a, b, k, i in res if k == "global flip" or k.endswith("only")]
    out(f"flips: {len(fl)}; lined up with an inner step change: {[(a, b) for a, b, i in fl if i] or 'none'}; "
        f"not lined up: {[(a, b) for a, b, i in fl if not i] or 'none'}")
    out(f"inner step changes without a flip: {[(a, b) for a, b, k, i in res if i and k == 'none'] or 'none'}")
    return r["v"], res


def selftest():
    Ds = [17.75, 18.0, 18.0625, 18.125, 18.1875, 18.25, 18.5]
    rows = rr.planted(Ds, [-1, -1, -1, -1, 1, 1, 1], [1, 1, 1, 1, -1, -1, -1])          # global flip at 18.125 -> 18.1875
    base = {"log": 100, (0.02, 0.05): 30, (0.3, 0.4): 120}
    steps = {D: {**base, (0.3, 0.4): 120 - i} for i, D in enumerate(Ds)}                 # outer changes everywhere
    steps[18.1875]["log"] = steps[18.25]["log"] = steps[18.5]["log"] = 101                # an inner change at 18.125 -> 18.1875 only
    v, res = table(rows, steps, out=lambda *a: None)
    ok1 = v == "global flip" and [(a, b) for a, b, k, i in res if i] == [(18.125, 18.1875)] and \
        [(a, b, i) for a, b, k, i in res if k == "global flip"] == [(18.125, 18.1875, True)]
    rows2 = rr.planted(Ds, [-1] * 7, [1] * 6 + [-1])
    lines = []
    table(rows2, steps, out=lines.append)
    ok2 = any("ruling: a root crossed 2.60, orientations compare from the 1.20 side" in l for l in lines)
    print(f"planted: a global flip at 18.125 -> 18.1875 lined up with the inner change there: {'PASS' if ok1 else 'FAIL'}")
    print(f"planted: 2.60 alone flips at 18.25 -> 18.5, the ruling's text names the 1.20 side: {'PASS' if ok2 else 'FAIL'}")
    print(f"selftest: {'PASS' if ok1 and ok2 else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    import numpy as np
    WTM = os.environ.get("P4_WT_MATTER", "/Users/nathan/Source/choptuik-1025/solver/matter")
    sys.path.insert(0, WTM); os.chdir(WTM)
    from dss_ell import DSSEll, NODES_STD
    rows = [json.loads(l) for l in open(args[0])]
    steps = {}
    for item in args[1].split(","):
        recf, st, D = item.split(":"); D = float(D)
        rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
        z = np.load(st)
        S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk") or 1)
        steps[D] = S.freeze_from(z, rec["kappa"])
        assert sum(steps[D].values()) == rec["steps"], f"D {D}: step total is not the record's"
    print(f"{os.path.basename(args[0])}: {len(rows)} records; step counts of {len(steps)} states (totals equal the records)")
    table(rows, steps)
