"""#961 line 5's verdict from the steps' records, stdlib only. Usage: python3 summary961.py RAWFOLDER [--mutate series]
Bars, fixed by the issue before the run: (a) and (b) both accepted at the same a; |Delta(b) - Delta(a)| <= 1e-40 (delta_b_a.log,
eight parts summed exactly by delta_cmp961.py); (b)'s series seconds (t_coef, with base_lu kept, so the series alone) at most
1/1.5 of (a)'s; control |Delta(c) - Delta(a)| > 1e-40 (delta_c_a.log). Reported, not judged: (d)'s a and its seconds per unit D
(series t_coef, the accepted attempt's re-seed plus corrector seconds, and the stage's wall for the whole step) against (b)'s.
--mutate series puts (a)'s t_coef in (b)'s place, which must make the series bar FAIL (exit 1)."""
import json
import re
import sys


def rec(folder, d):
    with open(f"{folder}/{d}/anm_run.jsonl") as f:
        r = [json.loads(x) for x in f if x.strip()]
    assert len(r) == 1, (d, len(r))
    return r[0]


def accepted(r):
    return [a for a in r["attempts"] if a["accepted"]]


def wall(folder, name):
    with open(f"{folder}/exits_961.txt") as f:
        for line in f:
            m = re.match(rf"961 {name} exit (\d+) wall (\d+)s", line)
            if m:
                return int(m.group(2))
    raise SystemExit(f"no exit line for {name}")


def diff_of(folder, log):
    with open(f"{folder}/{log}") as f:
        m = re.search(r"\|B - A\| (\S+), bound", f.read())
    return float(m.group(1))


def attempt_s(a):
    """re-seed seconds plus the corrector's, of one attempt (the rest of an attempt is the prediction and plan, seconds)"""
    return (a["reseed"]["seconds"] if a.get("reseed") else 0.0) + a["t_corr"]


def main(argv):
    folder = argv[0]
    mutate = "--mutate" in argv and argv[argv.index("--mutate") + 1]
    A, B, C, D = (rec(folder, d) for d in ("step_off", "step_on", "step_ks250", "step_n31"))
    if mutate == "series":
        B = dict(B, t_coef=A["t_coef"])
    aa, ab, ac, ad = (accepted(r) for r in (A, B, C, D))
    ok = True
    def check(name, passed, text):
        nonlocal ok
        ok &= passed
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {text}")
    check("(a) and (b) accepted at the same a", len(aa) == len(ab) == 1 and aa[0]["a"] == ab[0]["a"],
          f"a {aa[0]['a']} and {ab[0]['a']}, attempts {len(A['attempts'])} and {len(B['attempts'])}")
    d_ba = diff_of(folder, "delta_b_a.log")
    check("|Delta(b) - Delta(a)| <= 1e-40", d_ba <= 1e-40, f"{d_ba:.3e}")
    ratio = A["t_coef"] / B["t_coef"]
    check("(b)'s series at most 1/1.5 of (a)'s", B["t_coef"] <= A["t_coef"] / 1.5,
          f"{B['t_coef']:.1f} s against {A['t_coef']:.1f} s, ratio {ratio:.3f} (bar 1.5, base_lu {A['base_lu']}, {B['base_lu']})")
    d_ca = diff_of(folder, "delta_c_a.log")
    check("control |Delta(c) - Delta(a)| > 1e-40", d_ca > 1e-40, f"{d_ca:.3e}, (c) accepted {len(ac)} at a {ac[0]['a'] if ac else None}")
    print("\nreported, not judged ((d): N 31, a_rule reseed, a_scale 0.0715; (b): N 24, the default rule)")
    print(f"{'':28} {'(b)':>12} {'(d)':>12}")
    wb, wd = wall(folder, "step_on"), wall(folder, "step_n31")
    rows = [("accepted a", ab[0]["a"], ad[0]["a"]),
            ("attempts", len(B["attempts"]), len(D["attempts"])),
            ("series s", B["t_coef"], D["t_coef"]),
            ("accepted attempt s", attempt_s(ab[0]), attempt_s(ad[0])),
            ("all attempts s", sum(attempt_s(a) for a in B["attempts"]), sum(attempt_s(a) for a in D["attempts"])),
            ("step wall s (stage)", wb, wd)]
    for n, x, y in rows:
        print(f"{n:28} {x:12.4f} {y:12.4f}")
    for n, x, y in rows[2:]:
        print(f"{n + ' per unit D':28} {x / ab[0]['a']:12.1f} {y / ad[0]['a']:12.1f}   (d)/(b) {(y / ad[0]['a']) / (x / ab[0]['a']):.3f}")
    print("\nsummary", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
