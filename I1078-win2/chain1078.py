"""#1078 on win2: the chain after the hp build (criteria: issue comments 7139543531 and 7139651998).

0. wait for build.done; hpkernel must import.
1. mode_matched.py toy (exit 0), toy --mutate=shift (exit 1), mode_matched_bracket.py selftest (0), --mutate=shift (1).
2. mode_matched.py four at M' 96 (exit 0), compared with dh370's raw I1083-dh370/four.jsonl: same signs, m 6, 1266
   matched steps, |ln - ln_dh370| <= 1e-9 at all four, else STOP (bit identity reported either way).
3. D_m scan at M' 96, the 0.25 grid 4.5..7.5.
4. a bracket root (mode_matched_bracket.py) for each sign change of that grid.
5. the 0.1 grid's other 24 points; a bracket root for each sign change of the 0.1 grid not holding a root of step 4.
6. with exactly one accepted root at M' 96: the same root at M' 128 and M' 160 (HP_DENSE_M_MAX=160), bracket
   r96 -+ 2e-4, widened to 2e-3 and 2e-2 while its ends agree in sign; then M' 96 at hmax 0.001 the same way.
   With 0 or several roots it stops after step 5 (the choice is the coordinator's).
Each subprocess runs at the launcher's priority (BelowNormal) with 6 threads and a cap; on the cap its tree is killed
(taskkill /T /F /PID of its own pid). A Traceback in a log or an unwanted exit stops the chain (STOP_<step>.txt).
"""
import json
import math
import os
import subprocess
import sys
import time

OUT = r"D:\choptuik-raw-i1078\I1078-win2"
RAW = r"D:\choptuik-raw-i1078"
HP = r"D:\choptuik-i1078dm\hp"
PY = r"C:\Users\nathan\Source\venv-i1078\Scripts\python.exe"
S96 = RAW + r"\I1072-dh370\states3\tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz"
S128 = RAW + r"\I1072-dh370\states3\tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635.npz"
S160 = RAW + r"\I1072-dh370\in3\tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz"
REF4 = RAW + r"\I1083-dh370\four.jsonl"
COARSE = [round(4.5 + 0.25 * i, 10) for i in range(13)]
FINE = [x for x in (round(4.5 + 0.1 * i, 10) for i in range(31)) if all(abs(x - c) > 1e-9 for c in COARSE)]
PIVOT_BAR = 1e-20


def stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())


def step(msg):
    with open(os.path.join(OUT, "steps_1078.txt"), "a") as fh:
        fh.write(f"{stamp()} {msg}\n")


def stop(name, why):
    with open(os.path.join(OUT, f"STOP_{name}.txt"), "w") as fh:
        fh.write(f"STOP {name}: {why} ({stamp()})\n")
    step(f"STOP {name}: {why}")
    with open(os.path.join(OUT, "chain.done"), "w") as fh:
        fh.write(f"stopped at {name} {stamp()}\n")
    sys.exit(1)


def run(name, want, cap, script, *args, env_extra=None):
    """run hp/<script> args with a cap in seconds; returns the exit code; stops the chain on a Traceback, a cap or an
    exit not in want"""
    env = dict(os.environ, OMP_NUM_THREADS="6", OPENBLAS_NUM_THREADS="6", MKL_NUM_THREADS="6",
               PYTHONIOENCODING="utf-8")
    env.pop("HP_DENSE_M_MAX", None)
    env.pop("HP_MODE_EQUIL", None)
    env.update(env_extra or {})
    log = os.path.join(OUT, name + ".log")
    t0 = time.time()
    with open(log, "w") as fh:
        fh.write(f"# {stamp()} cmd: {script} {' '.join(args)} env+{env_extra or {}}\n")
        fh.flush()
        p = subprocess.Popen([PY, "-u", script, *args], cwd=HP, stdout=fh, stderr=subprocess.STDOUT, env=env)
        step(f"{name}: pid {p.pid}, cap {cap} s: {script} {' '.join(args)}")
        try:
            rc = p.wait(timeout=cap)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            p.wait()
            step(f"{name}: cap {cap} s reached, tree of pid {p.pid} killed")
            stop(name, "cap reached")
    txt = open(log, encoding="utf-8", errors="replace").read()
    last = txt.strip().splitlines()[-1][:300] if txt.strip() else ""
    step(f"{name}: exit {rc} (want {want}), {time.time() - t0:.0f} s; {last}")
    with open(os.path.join(OUT, "exit_codes.txt"), "a") as fh:
        fh.write(f"{name} {rc}\n")
    if "Traceback" in txt:
        stop(name, "an exception (see the log)")
    if rc not in want:
        stop(name, f"exit {rc} not in {want}")
    return rc


def rows(path, kind=None):
    if not os.path.exists(path):
        return []
    out = [json.loads(l) for l in open(path) if l.strip()]
    return [r for r in out if kind is None or r.get("kind") == kind]


def changes(scan):
    """adjacent sign changes (a, b) of resolved det rows, sorted by lam"""
    pts = sorted({r["lam"]: r for r in scan if r["pmin"] / r["pmax"] > PIVOT_BAR}.values(), key=lambda r: r["lam"])
    return [(pts[i]["lam"], pts[i + 1]["lam"]) for i in range(len(pts) - 1) if pts[i]["sign"] != pts[i + 1]["sign"]]


def bracket(name, state, a, b, seed, extra=(), env_extra=None, cap=6 * 3600):
    o = os.path.join(OUT, name + ".jsonl")
    rc = run(name, (0, 1), cap, "mode_matched_bracket.py", "root", o, state, repr(a), repr(b), f"--seed={seed}",
             "--xtol=1e-11", "--threads=6", *extra, env_extra=env_extra)
    v = [r for r in rows(o, "verdict")][-1]
    return v if rc == 0 and v["passed"] else None


def follow(tag, state, r0, extra=(), env_extra=None, cap_det=3600):
    """the root near r0 on another state or plan: ends at r0 -+ w (det rows in scan_<tag>.jsonl), widened while they
    agree in sign, then a bracket root"""
    sc = os.path.join(OUT, f"scan_{tag}.jsonl")
    for w in (2e-4, 2e-3, 2e-2):
        a, b = r0 - w, r0 + w
        run(f"ends_{tag}_w{w:g}", (0,), 3 * cap_det, "mode_matched.py", "det", sc, state, repr(a), repr(b),
            "--threads=6", *extra, env_extra=env_extra)
        got = {r["lam"]: r for r in rows(sc, "det")}
        if got[a]["sign"] != got[b]["sign"]:
            v = bracket(f"root_{tag}", state, a, b, sc, extra, env_extra, cap=15 * cap_det)
            step(f"follow {tag}: root {v['lam'] if v else None!r} in [{a!r}, {b!r}] ({'PASS' if v else 'FAIL'})")
            return v
        step(f"follow {tag}: same sign {got[a]['sign']:+.0f} at r0 -+ {w:g}, widening")
    step(f"follow {tag}: no sign change within r0 -+ 2e-2")
    return None


def main():
    step("chain1078 start")
    while not os.path.exists(os.path.join(OUT, "build.done")):
        time.sleep(60)
    ver = open(os.path.join(OUT, "versions.txt"), encoding="utf-8", errors="replace").read()
    if "isa" not in ver or "Traceback" in ver:
        stop("build", "hpkernel does not import (versions.txt)")
    step("build.done seen, hpkernel imports")
    # 1. toy and the bracket selftest, with their controls
    run("1_toy", (0,), 1800, "mode_matched.py", "toy")
    run("1b_toy_mutate_shift", (1,), 1800, "mode_matched.py", "toy", "--mutate=shift")
    run("1c_bracket_selftest", (0,), 600, "mode_matched_bracket.py", "selftest")
    run("1d_bracket_selftest_shift", (1,), 600, "mode_matched_bracket.py", "selftest", "--mutate=shift")
    # 2. four against dh370
    f4 = os.path.join(OUT, "four.jsonl")
    run("2_four", (0,), 4 * 3600, "mode_matched.py", "four", f4, S96, "--threads=6")
    mine, ref = rows(f4, "four"), rows(REF4, "four")
    lines, ok, bit = [], len(mine) == 4 and len(ref) == 4, True
    for x, y in zip(mine, ref):
        d = x["ln"] - y["ln"]
        bit &= x["ln"] == y["ln"] and x["sign"] == y["sign"] and x["pmin"] == y["pmin"] and x["pmax"] == y["pmax"]
        ok &= x["lam"] == y["lam"] and x["sign"] == y["sign"] and abs(d) <= 1e-9 and x["m"] == 6 and x["steps_m"] == 1266
        lines.append(f"lam {x['lam']!r}: win2 sign {x['sign']:+.0f} ln {x['ln']!r} pmin {x['pmin']!r} pmax {x['pmax']!r} "
                     f"| dh370 sign {y['sign']:+.0f} ln {y['ln']!r} pmin {y['pmin']!r} pmax {y['pmax']!r} | diff ln {d:+.3e}")
    with open(os.path.join(OUT, "four_compare.txt"), "w") as fh:
        fh.write("\n".join(lines) + f"\nbit-identical (sign, ln, pmin, pmax): {bit}\nsame signs, m 6, 1266 steps, "
                 f"|diff ln| <= 1e-9: {ok}\n")
    step(f"2_four compare: bit-identical {bit}, within 1e-9 {ok}")
    if not ok:
        stop("2_four_compare", "win2's four rows differ from dh370's beyond 1e-9 or in sign/layout (four_compare.txt)")
    with open(os.path.join(OUT, "check.done"), "w") as fh:
        fh.write(f"{stamp()} bit-identical {bit}\n")
    # 3. the 0.25 scan
    sc = os.path.join(OUT, "scan_m96.jsonl")
    run("3_scan_m96_coarse", (0,), 13 * 3600, "mode_matched.py", "det", sc, S96, *map(repr, COARSE), "--threads=6")
    roots = []
    for a, b in changes(rows(sc, "det")):
        v = bracket(f"4_root_m96_{a:.2f}_{b:.2f}", S96, a, b, sc)
        roots.append((a, b, v))
    step(f"coarse roots: {[(a, b, v['lam'] if v else None) for a, b, v in roots]}")
    # 5. the 0.1 fill
    run("5_scan_m96_fine", (0,), 24 * 3600, "mode_matched.py", "det", sc, S96, *map(repr, FINE), "--threads=6")
    for a, b in changes(rows(sc, "det")):
        if any(v and a <= v["lam"] <= b for _, _, v in roots):
            continue
        v = bracket(f"5_root_m96_{a:.2f}_{b:.2f}", S96, a, b, sc)
        roots.append((a, b, v))
    acc = [v for _, _, v in roots if v]
    step(f"M' 96 roots: {[(a, b, v['lam'] if v else None) for a, b, v in roots]}; accepted {len(acc)}")
    with open(os.path.join(OUT, "m96.done"), "w") as fh:
        fh.write(f"{stamp()} accepted roots {[v['lam'] for v in acc]} of {len(roots)} sign changes\n")
    if len(acc) != 1 or len(roots) != 1:
        stop("6_ladder", f"{len(roots)} sign changes, {len(acc)} accepted roots at M' 96: the ladder waits for the coordinator")
    r96 = acc[0]["lam"]
    # 6. M' 128, M' 160, hmax 0.001
    v128 = follow("m128", S128, r96, cap_det=2 * 3600)
    v160 = follow("m160", S160, v128["lam"] if v128 else r96, env_extra={"HP_DENSE_M_MAX": "160"}, cap_det=4 * 3600)
    vh = follow("m96_h0.001", S96, r96, extra=("--hmax=0.001",), cap_det=3 * 3600)
    step(f"ladder: r96 {r96!r}, r128 {v128 and v128['lam']!r}, r160 {v160 and v160['lam']!r}, r96 hmax 0.001 "
         f"{vh and vh['lam']!r}")
    with open(os.path.join(OUT, "chain.done"), "w") as fh:
        fh.write(f"done {stamp()}\n")


if __name__ == "__main__":
    main()
