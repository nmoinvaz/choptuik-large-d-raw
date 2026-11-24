"""#1084 probe: run a value_mp module's value_point / value_v unchanged, observing every residual call and every
linear solve through wrappers that return the wrapped functions' results untouched. At each Jacobian refresh it
also forms the step the previous (stale) Jacobian would have taken from the same v (one more lu_solve, no residual
call) and compares its bits with the fresh step's.

    python probe.py MODDIR point A WF F3RE F3IM [--iters=12] [--log=FILE.jsonl]
    python probe.py MODDIR pointv A WF --M=5 --v=B3,C3,... [--iters=8] [--log=FILE.jsonl]
"""
import json
import sys
import time

moddir = sys.argv[1]
sys.path.insert(0, moddir)
import mpmath as mpm  # noqa: E402
import value_mp as VM  # noqa: E402

args = [a for a in sys.argv[2:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[2:] if a.startswith("--") and "=" in a)
log = open(opts["log"], "a") if "log" in opts else None
assert VM.__file__.startswith(moddir.rstrip("/")), VM.__file__

_res = VM.IM.residual_demixed
_lu = mpm.lu_solve
state = dict(lastJ=None, lastrhs=None, last_v=None, last_vn=None, calls=0)
events = []


def emit(d):
    d["t"] = round(time.time() - T0, 1)
    events.append(d)
    if log:
        log.write(json.dumps(d) + "\n")
        log.flush()
    print(json.dumps(d), file=sys.stderr, flush=True)


def ulp(x):
    if x == 0:
        return mpm.mpf(2) ** (-mpm.mp.prec)
    return mpm.mpf(2) ** (int(mpm.floor(mpm.log(abs(x), 2))) - mpm.mp.prec + 1)


def res(x, M=3, r1="0.17", NTH=64, p=40, margin=12):
    out, info = _res(x, M, r1, NTH=NTH, p=p, margin=margin)
    state["calls"] += 1
    v = tuple(mpm.mpf(t) for t in x[2:])
    emit(dict(ev="res", dps=mpm.mp.dps, call=state["calls"], maxr=mpm.nstr(max(abs(t) for t in out[2:]), 4),
              v=[mpm.nstr(t, mpm.mp.dps + 8) for t in v], R=[mpm.nstr(t, mpm.mp.dps + 8) for t in out[:2]],
              r=[mpm.nstr(t, mpm.mp.dps + 8) for t in out[2:]]))
    return out, info


def lu(J3, rhs):
    out = _lu(J3, rhs)
    cv = state.get("cur_v")
    emit(dict(ev="lu", dps=mpm.mp.dps, n0=mpm.nstr(max(abs(rhs[i]) for i in range(rhs.rows)), 4),
              refresh=state["lastJ"] is not None and J3 is not state["lastJ"],
              dv_ulps=None if cv is None else [mpm.nstr(abs(out[i]) / ulp(cv[i]), 3) for i in range(rhs.rows)]))
    if state["lastJ"] is not None and J3 is not state["lastJ"]:
        # a refresh (or the second precision's start): the step the previous Jacobian would take from this v
        dv_old = _lu(state["lastJ"], rhs)
        n = J3.rows
        rn = max(abs(rhs[i]) for i in range(n))
        d = []
        same = True
        for i in range(n):
            vi = state["cur_v"][i] if state.get("cur_v") is not None else None
            if vi is None:
                same = None
                break
            a, b = vi + out[i], vi + dv_old[i]
            same &= (a == b)
            d.append(float(abs(a - b) / ulp(vi)))
        emit(dict(ev="refresh", dps=mpm.mp.dps, n0=mpm.nstr(rn, 4), same_bits=same, dvn_ulps=d,
                  dv=[mpm.nstr(out[i], 4) for i in range(n)],
                  dJ_rel=mpm.nstr(max(abs(J3[i, k] - state["lastJ"][i, k]) for i in range(n) for k in range(n))
                                  / max(abs(J3[i, k]) for i in range(n) for k in range(n)), 3)))
    state["lastJ"] = J3
    return out


VM.IM.residual_demixed = res
mpm.lu_solve = lu

# value_mp's solve forms vn = v + dv with the v it holds; the probe needs that v at each lu_solve: track it from the
# right-hand side's residual call (the v whose residual is -rhs)
_orig_matrix = mpm.matrix
_vres = {}


def res2(x, M=3, r1="0.17", NTH=64, p=40, margin=12):
    out, info = res(x, M, r1, NTH=NTH, p=p, margin=margin)
    _vres[tuple(mpm.mpf(t) for t in out[2:])] = tuple(mpm.mpf(t) for t in x[2:])
    return out, info


def lu2(J3, rhs):
    key = tuple(-rhs[i] for i in range(rhs.rows))
    state["cur_v"] = _vres.get(key)
    return lu(J3, rhs)


VM.IM.residual_demixed = res2
mpm.lu_solve = lu2

T0 = time.time()
it = int(opts.get("iters", 12))
if args[0] == "point":
    row = VM.value_point(args[1], args[2], args[3], args[4], iters=it)
else:
    M = int(opts["M"])
    row = VM.value_v(args[1], args[2], opts["v"].split(","), M, iters=it)
row["J"] = None
emit(dict(ev="row", row=row))
print(json.dumps(row), flush=True)
