"""#1104 winb, the re-solve of the k_c 143 D 23.0 state at kappa 0.5 (t5's bars, #1104 comment 7225436553 of 2026-11-27 18:23 UTC): the last record of RECORD must be D 23.0, k_c 143, kappa 0.5 with |F| <= 5e-10
and steps in 6455-6719 (6587 +- 132 = 1.4 x the kappa 0.7 count 4705, +- 2%). Same form as dh370's gate_R1.py (raw I1101-dh370/R1). usage: gate_k050_1104.py RECORD [--mutate=f|steps] | --selftest
Exit 0 only if all hold. Controls (each must exit 1): my kappa 0.7 record l1kc143winbd23.jsonl (kappa 0.7, steps 4705), and --mutate=f / --mutate=steps on a record forced to violate that clause."""
import json, sys


def clauses(r):
    return dict(D=r["D"] == 23.0, kc=r["kc"] == 143, kappa=r["kappa"] == 0.5, F=r["F"] <= 5e-10, steps=6455 <= r["steps"] <= 6719)


def selftest():
    ok = True
    base = dict(D=23.0, kc=143, kappa=0.5, F=3.2e-10, steps=6587)
    for name, r, want in (("a record at the bars' centre", base, True), ("|F| 6e-10", dict(base, F=6e-10), False), ("steps 6454", dict(base, steps=6454), False),
                          ("steps 6455", dict(base, steps=6455), True), ("steps 6719", dict(base, steps=6719), True), ("steps 6720", dict(base, steps=6720), False),
                          ("kappa 0.7 with 4705 steps", dict(base, kappa=0.7, steps=4705), False), ("k_c 127", dict(base, kc=127), False), ("D 22.875", dict(base, D=22.875), False)):
        got = all(clauses(r).values())
        print(f"planted: {name}: verdict {got}, expected {want}: {'PASS' if got == want else 'FAIL'}")
        ok = ok and got == want
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    f = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    m = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")
    r = [json.loads(l) for l in open(f) if l.strip()][-1]
    if m == "f":
        r["F"] = 6e-10
    if m == "steps":
        r["steps"] = 6454
    c = clauses(r)
    print(f"|F| {r['F']:.6e}, steps {r['steps']}, Delta {r['Delta']!r}, kappa {r['kappa']}, kc {r['kc']}, D {r['D']}: " + " ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in c.items()))
    sys.exit(0 if all(c.values()) else 1)
