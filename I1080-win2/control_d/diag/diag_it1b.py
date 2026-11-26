"""#1080 walk d, diagnosis of iteration 1, second run: diag_it1.py's call, with a hook on the Taylor stepper that prints, every
100 Taylor steps, the position xi of the integration, max|Y| and the seconds. A stepper that crowds towards one xi with Y
growing is stuck at a pole of the solution near the path; steady progress along the path is a slow but finite call.

    python -u diag_it1b.py ROWS.jsonl
"""
import json
import sys
import time

sys.path.insert(0, r"D:\choptuik-i1080d\solver\inner_stokes")
import mpmath as mp  # noqa: E402
import inner_mp as IM  # noqa: E402
import value_mp as VM  # noqa: E402

row = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]
A, wf = row["A"] + float(row["dA"]), row["wf"] + float(row["dwf"])
print(f"centre of iteration {row['it'] + 1}: A {A!r} wf {wf!r}", flush=True)
t0, n, nt = time.time(), [0], [0]
orig_res, orig_tay = IM.residual_demixed, IM.InnerMP.taylor


def res_w(*a, **k):
    nt[0] = 0
    out = orig_res(*a, **k)
    n[0] += 1
    print(f"  call {n[0]} dps {mp.mp.dps}: max|r3..r5| {mp.nstr(max(abs(x) for x in out[0][2:]), 3)}, steps {out[1]['steps']}, "
          f"ymax {mp.nstr(out[1]['ymax'], 3)}, {time.time() - t0:.0f} s", flush=True)
    return out


def tay_w(self, xc, Y, p):
    nt[0] += 1
    if nt[0] % 100 == 1:
        ym = max(abs(v) for part in Y for v in part)
        print(f"    call {n[0] + 1} taylor {nt[0]}: |xi| {mp.nstr(abs(xc), 8)} arg {mp.nstr(mp.arg(xc), 8)} max|Y| {mp.nstr(ym, 3)}, "
              f"{time.time() - t0:.0f} s", flush=True)
    return orig_tay(self, xc, Y, p)


IM.residual_demixed = res_w
IM.InnerMP.taylor = tay_w
res = VM.value_v(repr(A), repr(wf), list(row["F3"]), 5, r1="0.17", J=row["J_inner"], want_J=True)
res.pop("J", None)
print(json.dumps(res), flush=True)
print(f"done: {n[0]} calls, {time.time() - t0:.0f} s", flush=True)
