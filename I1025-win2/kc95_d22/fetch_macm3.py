#!/usr/bin/env python3
"""fetch_macm3.py D OUTDIR [--poll S] [--max-hours H]: wait until macm3's k_c 87 leg (raw I1025-macm3/kc87_leg2/b/, tag l1kc87Lmacm3b) has
pushed the state of D and a record row for D, then download both (through `gh api`, the raw contents) and verify each against the blob sha the
listing gives. Writes OUTDIR/sol_l1kc87Lmacm3b_D{D:.4f}.npy (the name ell_refine reads), OUTDIR/l1kc87Lmacm3b.jsonl (the record file as pushed)
and OUTDIR/fetched.txt (D, blobs, commit time, the record row). Exit 0 when fetched, 1 on a blob mismatch, 2 on timeout.
options: --path=RAWFOLDER --tag=TAG (default I1025-macm3/kc87_leg2/b, l1kc87Lmacm3b)
usage of the self test: fetch_macm3.py --selftest [--mutate]   (the blob function against git hash-object, the row finder on planted rows; --mutate must exit 1)"""
import base64
import hashlib
import json
import subprocess
import sys
import time

REPO = "nmoinvaz/choptuik-large-d-raw"
PATH = "I1025-macm3/kc87_leg2/b"
TAG = "l1kc87Lmacm3b"


def blob(b):
    h = hashlib.md5 if "--mutate" in sys.argv else hashlib.sha1   # --mutate: a wrong hash, which the selftest must catch
    return h(b"blob %d\0" % len(b) + b).hexdigest()


def gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("gh %s: %s" % (" ".join(args[:2]), r.stderr.decode(errors="replace")[:300]))
    return r.stdout


def listing():
    return {x["name"]: x["sha"] for x in json.loads(gh(["api", "repos/%s/contents/%s" % (REPO, PATH)]))}


def raw(name):
    return gh(["api", "-H", "Accept: application/vnd.github.raw", "repos/%s/contents/%s/%s" % (REPO, PATH, name)])


def find_row(jsonl_bytes, D):
    rows = [json.loads(l) for l in jsonl_bytes.decode().splitlines() if l.strip()]
    m = [r for r in rows if abs(r["D"] - D) < 1e-9]
    return m[-1] if m else None


def selftest():
    bad = []
    if blob(b"hello\n") != "ce013625030ba8dba906f756967f9e9ca394464a":
        bad.append("blob of 'hello\\n'")
    rows = b'{"D": 21.5, "F": 1}\n{"D": 21.53125, "F": 2}\n'
    if find_row(rows, 21.53125) is None or find_row(rows, 21.53125)["F"] != 2 or find_row(rows, 21.6) is not None:
        bad.append("row finder")
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    global PATH, TAG
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    for x in a:   # --path=RAWFOLDER --tag=TAG name another leg of macm3's (part b2: I1025-macm3/kc87_leg2/b2, l1kc87Lmacm3b2)
        if x.startswith("--path="):
            PATH = x[len("--path="):]
        if x.startswith("--tag="):
            TAG = x[len("--tag="):]
    a = [x for x in a if not x.startswith("--path=") and not x.startswith("--tag=")]
    D, out = float(a[0]), a[1]
    poll = float(a[a.index("--poll") + 1]) if "--poll" in a else 60.0
    maxh = float(a[a.index("--max-hours") + 1]) if "--max-hours" in a else 24.0
    names = ["sol_%s_D%.6f.npy" % (TAG, D), "sol_%s_D%.4f.npy" % (TAG, D)]
    t0 = time.time()
    while True:
        try:
            ls = listing()
            nm = next((n for n in names if n in ls), None)
            if nm and (TAG + ".jsonl") in ls:
                rec = raw(TAG + ".jsonl")
                row = find_row(rec, D)
                if row is not None:
                    st = raw(nm)
                    if blob(st) != ls[nm] or blob(rec) != ls[TAG + ".jsonl"]:
                        # the listing changed between the calls: look again
                        time.sleep(5)
                        continue
                    open("%s/sol_%s_D%.4f.npy" % (out, TAG, D), "wb").write(st)
                    open("%s/%s.jsonl" % (out, TAG), "wb").write(rec)
                    open("%s/fetched.txt" % out, "w").write(
                        "fetched %s UTC\nstate %s blob %s (%d bytes)\nrecord %s.jsonl blob %s (%d rows)\nrow %s\n" % (
                            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), nm, ls[nm], len(st), TAG, ls[TAG + ".jsonl"],
                            len([1 for l in rec.decode().splitlines() if l.strip()]), json.dumps({k: row[k] for k in ("D", "kc", "F", "steps", "constraint", "Delta", "h") if k in row})))
                    print("fetched", nm, ls[nm], flush=True)
                    return 0
            print("%s waiting for D %g (state %s, record row)" % (time.strftime("%H:%M:%S", time.gmtime()), D, "listed" if nm else "not listed"), flush=True)
        except Exception as e:  # network or gh error: log and try again
            print("%s error: %s" % (time.strftime("%H:%M:%S", time.gmtime()), e), flush=True)
        if time.time() - t0 > maxh * 3600:
            return 2
        time.sleep(poll)


if __name__ == "__main__":
    sys.exit(main())
