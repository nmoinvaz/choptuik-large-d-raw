"""a runner's reader for #907: the readings of the two continued walks, the one Jacobian and the widths, against the
issue's acceptance. usage: python read907.py I907_FOLDER [I897_FOLDER]"""
import json
import os
import sys

R = sys.argv[1]
I = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(R.rstrip("/\\")), "I897-winb")
BS = chr(92)


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def tail(s):
    return s.replace(BS, "/").split("/")[-1]


wd = {tail(r["state"]): r for r in jl(os.path.join(R, "width3.jsonl"))} if os.path.exists(os.path.join(R, "width3.jsonl")) else {}
out = {}
for n, D in (("up_10.0", 10.0), ("up_10.5", 10.5)):
    p = os.path.join(R, f"walk3_{n}.jsonl")
    if not os.path.exists(p):
        print(n, "not finished")
        continue
    k = jl(p)[-1]
    h = k["hist"]
    acc = h[:-1] if k["stalled"] else h
    d = [x["dDelta"] for x in acc]
    a = jl(os.path.join(I, f"walk2_{n}.jsonl"))[-1]
    end = k["Delta"]
    m10 = sum(d[-10:]) / len(d[-10:])
    m50 = sum(d[-50:]) / len(d[-50:])
    q = (d[-1] / d[-51]) ** (1 / 50) if len(d) > 51 and d[-51] != 0 and d[-1] / d[-51] > 0 else None
    q10 = (sum(d[-10:]) / sum(d[-60:-50])) ** (1 / 50) if len(d) > 60 and sum(d[-60:-50]) != 0 else None
    w = wd.get(f"walk3_{n}.npy")
    state = "stalled" if k["stalled"] else "settled" if k["settled"] else "not settled"
    print(f"{n}: {state} after {len(h)} Jacobians ({len(acc)} applied); start (#897 end) Delta {a['Delta']:.9f}; "
          f"end Delta {end:.9f}, moved {end - a['Delta']:+.4e}")
    print(f"    abs(F) walk {acc[-1]['F']:.4e}" + (f"; width abs(F) {w['F']:.4e}, W {w['W']:.4e}, Newton {w['newton_dDelta']:+.4e}, "
          f"g {w['g_svd']:.5e}/{w['g_solve']:.5e} agree {w['agree']}, smax {w['smax']:.2f}, smallest {w['smallest'][0]['s']:.2e}" if w else ""))
    print(f"    steps: first {d[0]:+.4e}, last {d[-1]:+.4e}, mean of last 10 {m10:+.4e}, of last 50 {m50:+.4e}")
    if q is not None:
        shrink = 1 - q
        print(f"    last 50 steps: decay factor {q:.6f} per Jacobian, i.e. 1 part in {1 / shrink:.0f} ({shrink:.3e}); "
              f"geometric rest {d[-1] * q / (1 - q):+.4e}, so the geometric end {end + d[-1] * q / (1 - q):.6f}")
    if q10 is not None:
        print(f"    mean of last 10 against mean of steps 51-60 back: decay factor {q10:.6f} per Jacobian (1 part in {1 / (1 - q10):.0f})")
    small = [x["jac"] for x in acc if abs(x["dDelta"]) < 1e-9]
    print(f"    steps below 1e-9: {small}; the steps are non-increasing in size at the end: "
          f"{all(abs(d[i + 1]) <= abs(d[i]) * 1.0001 for i in range(len(d) - 51, len(d) - 1))}")
    out[n] = (end, d, q)

if "up_10.5" in out:
    end, d, q = out["up_10.5"]
    shrink = 1 - q if q else None
    geo = abs(end - 1.12538) <= 1e-3 and shrink is not None and abs(shrink - 1 / 730) <= 0.3 / 730
    tow = end > 1.130 or (shrink is not None and shrink <= 0)
    print("D 10.5 acceptance: end within 1e-3 of 1.12538:", abs(end - 1.12538) <= 1e-3, f"({end - 1.12538:+.4e})",
          "; decay rate within 30% of 1/730:", shrink is not None and abs(shrink - 1 / 730) <= 0.3 / 730,
          f"({shrink:.3e} against {1 / 730:.3e})" if shrink else "",
          "; end above 1.130:", end > 1.130, "=>", "geometric" if geo else "toward 1.138" if tow else "undecided")
if "up_10.0" in out:
    end = out["up_10.0"][0]
    print(f"D 10.0 acceptance: end within 2e-4 of 1.15209: {abs(end - 1.15209) <= 2e-4} ({end - 1.15209:+.4e}); Newton's estimate 1.15177")

p = os.path.join(R, "jac1_up_10.5.jsonl")
if os.path.exists(p):
    k = jl(p)[-1]
    h = k["hist"]
    print(f"jac1_up_10.5: {len(h)} Jacobian, abs(F) {h[-1]['F']:.4e}, Delta {h[-1]['Delta']:.12f}, change {h[-1]['dDelta']:+.4e}, "
          f"stalled {k['stalled']}")
