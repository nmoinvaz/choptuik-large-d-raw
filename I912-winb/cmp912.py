"""#912: this run's s3.json and s5.json against the Mac's (the committed blob and the working copy), bytes and fields.
usage: python cmp912.py RAWROOT MINE_FOLDER"""
import json
import subprocess
import sys

root, mine = sys.argv[1], sys.argv[2]


def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + f"[{i}]")
    else:
        yield p, x


for f in ("s3", "s5"):
    a = open(f"{mine}/{f}.json", "rb").read()
    blob = subprocess.run(["git", "-C", root, "show", f"HEAD:I865-mac/{f}.json"], capture_output=True, check=True).stdout
    wc = open(f"{root}/I865-mac/{f}.json", "rb").read()
    print(f"{f}: mine {len(a)} bytes ({a.count(b'\r')} CR), Mac blob {len(blob)} ({blob.count(b'\r')} CR), Mac working copy {len(wc)} "
          f"({wc.count(b'\r')} CR)")
    a_lf = a.replace(b"\r\n", b"\n")
    print(f"   mine with CRLF as LF equals the Mac's blob: {a_lf == blob}; equals the Mac's working copy: {a == wc}; "
          f"working copy with CRLF as LF equals the blob: {wc.replace(b'\r\n', b'\n') == blob}")
    A, B = dict(leaves(json.loads(a))), dict(leaves(json.loads(blob)))
    diff = [(p, A.get(p), B.get(p)) for p in sorted(set(A) | set(B)) if A.get(p) != B.get(p)]
    print(f"   {len(A)} fields against {len(B)}; differing fields: {len(diff)}")
    import re
    BALL = re.compile(r"^\[\s*([-+0-9.eE]+)\s*\+/-\s*([-+0-9.eE]+)\s*\]$")
    flo, balls, other = [], [], []
    for p, x, y in diff:
        if isinstance(x, float) and isinstance(y, float):
            flo.append((abs(x - y) / max(abs(x), abs(y)), p, x, y))
        elif isinstance(x, str) and isinstance(y, str) and BALL.match(x) and BALL.match(y):
            mx, my = BALL.match(x), BALL.match(y)
            balls.append((p, mx[1], my[1], float(mx[2]) / float(my[2]), mx[2], my[2]))
        else:
            other.append((p, x, y))
    print(f"   f64 fields: {len(flo)} differ, largest relative difference {max(flo)[0]:.2e} ({max(flo)[1]}), "
          f"median {sorted(flo)[len(flo) // 2][0]:.2e}" if flo else "   f64 fields: none differ")
    grp = {}
    for r_, p, x, y in flo:
        g = re.sub(r"\[\d+\]", "", p)
        grp.setdefault(g, []).append(r_)
    for g, v in sorted(grp.items()):
        print(f"      f64 array {g}: {len(v)} entries differ, largest relative difference {max(v):.2e}")
    for p, mx, my, r, rx, ry in balls:
        print(f"   ball {p}: midpoints {mx} against {my}{' (equal)' if mx == my else ' (DIFFER)'}, radii {rx} against {ry} (ratio {r:.4f})")
    for p, x, y in other:
        print(f"   other {p}: {x!r} against {y!r}")
    same = [p for p in A if A[p] == B.get(p)]
    print(f"   equal fields: {len(same)}: {', '.join(sorted(set(re.sub(r'\[\d+\]', '', p) for p in same)))}")
