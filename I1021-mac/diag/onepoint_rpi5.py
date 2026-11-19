"""#1021: one point of rpi5's #1013 step-1 box (argcount count, not a recount) through f_M3 of the argcount at CODE,
alone, with a log line per residual evaluation and per _refine3 / nested.inner call; the seed is the one argcount's
count passes (empty cache, the known zero's F_3); BOUNDS (JSON) go to f_M3 as args[4], and SIGALRM at BOUND_S + 60 s
is a backstop.
    python onepoint_rpi5.py CODE A0,A1 W0,W1 NA NWF PROCS A WF R1 BOUNDS BOUND_S"""
import faulthandler, json, resource, signal, sys, time, traceback, warnings
import numpy as np
code = sys.argv[1]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac

box = (tuple(map(float, sys.argv[2].split(","))), tuple(map(float, sys.argv[3].split(","))))
nA, nwf, procs = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
want, r1run, bounds, bound = (float(sys.argv[7]), float(sys.argv[8])), float(sys.argv[9]), json.loads(sys.argv[10]), int(sys.argv[11])


class Batch(Exception):
    pass


class Stop(ac.Multiplier):
    def raw(self, pts):
        todo, seen = [], set()
        for p in pts:
            k = self.key(p)
            if k not in self.vals and k not in seen:
                seen.add(k)
                todo.append(p)
        if todo:
            raise Batch([(p, self.seed(p)) for p in todo])


F = Stop(3, None, procs, None, r1=0.2, m3fix=True)
F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),
                             F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
try:
    ac.count(F, box, nA, nwf)
    raise SystemExit("no uncached point")
except Batch as e:
    todo = e.args[0]
idx = min(range(len(todo)), key=lambda i: abs(todo[i][0][0] - want[0]) + abs(todo[i][0][1] - want[1]))
p, seed = todo[idx]
print(f"first batch ({len(todo)}): {[(round(q[0], 4), round(q[1], 4)) for q, _ in todo]}")
print(f"point {idx}: A {p[0]!r} wf {p[1]!r} seed {seed!r}; xi1 {r1run}, bounds {bounds}", flush=True)

T0 = time.time()
I = ac._probe_inner_np()
import nested
ctx = {"who": "start", "steps": 0, "n": 0}
ivp = I.solve_ivp


def solve_ivp(*a, **k):
    sol = ivp(*a, **k)
    ctx["steps"] += len(sol.t)
    return sol


I.solve_ivp = solve_ivp
rd = I.residual_demixed


def residual_demixed(x, M, *a, **k):
    ctx["steps"], t = 0, time.time()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = rd(x, M, *a, **k)
    ctx["n"] += 1
    r3 = float(np.abs(out[2:]).max()) if np.all(np.isfinite(out)) else float("nan")
    print(f"{time.time() - T0:8.1f} s  eval {ctx['n']:4d}  {ctx['who']:10s} r1 {k.get('r1')}  max|v| {np.abs(x[2:]).max():.4g}  "
          f"|r3| {r3:.3g}  steps {ctx['steps']}  {time.time() - t:.2f} s  maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB"
          + (f"  warnings {sorted(set(str(x.message)[:40] for x in w))}" if w else ""), flush=True)
    return out


I.residual_demixed = residual_demixed
ref, cont, inner = ac._refine3, ac._continue3, nested.inner


def refine3(I_, A, wf, v, r1, **k):
    ctx["who"] = "refine3"
    print(f"{time.time() - T0:8.1f} s  _refine3 at r1 {r1} from v {v}", flush=True)
    out = ref(I_, A, wf, v, r1, **k)
    print(f"{time.time() - T0:8.1f} s  _refine3 end: v {out[0]}, |r3| {np.abs(out[1][2:]).max():.3g}", flush=True)
    ctx["who"] = "floor/res"
    return out


def inner_(A, wf, F3, r1, *a, **k):
    ctx["who"] = "nested"
    out = inner(A, wf, F3, r1, *a, **k)
    print(f"{time.time() - T0:8.1f} s  nested.inner at r1 {r1} end: F3 {out[0]}, r3 {out[2]:.3g}", flush=True)
    ctx["who"] = "after"
    return out


ac._refine3, nested.inner = refine3, inner_
faulthandler.dump_traceback_later(300, repeat=True)


def alarm(*_):
    print(f"{time.time() - T0:8.1f} s  BOUND {bound} s reached; stack:", flush=True)
    traceback.print_stack()
    sys.exit(3)


signal.signal(signal.SIGALRM, alarm)
signal.alarm(bound + 60)
res = ac.f_M3((p, seed, r1run, True, bounds))
print(f"{time.time() - T0:8.1f} s  f_M3 returned: {res[:7]}  fix {({k: v for k, v in res[7].items()} if len(res) > 7 else None)}", flush=True)
