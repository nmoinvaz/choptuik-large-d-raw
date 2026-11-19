p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\eval_1029.py"
s = open(p, encoding="utf-8").read()
a = s.index("def main():")
b = s.index('\n\nif __name__ == "__main__":')
new_main = r'''def fm(x, nd=4):
    """float formatting for normal sizes, mpmath's for numbers beyond a double"""
    if isinstance(x, (float, int)) or (hasattr(x, "imag") is False and abs(x) < 1e12):
        return f"{float(x):.{nd}f}" if abs(x) < 1e6 else f"{float(x):.2e}"
    return mp.nstr(x, 3)


def load_run(ns, wf, J):
    """K, f (complex; entries whose double overflowed, stored as Infinity, are rebuilt as mpc from the run log's 10 digits), and how many were rebuilt"""
    base = os.path.join(HERE, f"sigF_w{wf}_K25_J{J}.json")
    K, Jf, f = ns["load_f"](base)
    log = open(os.path.join(HERE, "logs", f"w{wf}_J{J}.log"), encoding="utf-8", errors="replace").read()
    pat = re.compile(r"k (\d+) nu (\d+): .* f \(([-+0-9.e]+) ([+-]) ([0-9.e]+)j\)")
    fixed = 0
    for m in pat.finditer(log):
        k, nu = int(m.group(1)), int(m.group(2))
        z = f.get((k, nu))
        if z is not None and not (np.isfinite(z.real) and np.isfinite(z.imag)):
            f[(k, nu)] = mp.mpc(mp.mpf(m.group(3)), (-1 if m.group(4) == "-" else 1) * mp.mpf(m.group(5)))
            fixed += 1
    return K, Jf, f, fixed


def main():
    ns = load_tp()
    mp.mp.dps = 30
    allj = {}
    for z in ZEROS:
        S = {}
        for J in JS:
            p = os.path.join(HERE, f"sigF_w{z['wf']}_K25_J{J}.json")
            if not os.path.isfile(p):
                print(f"{z['name']} J {J}: {os.path.basename(p)} missing")
                continue
            K, Jf, f, fixed = load_run(ns, z["wf"], J)
            d = json.load(open(p))
            S[J] = series(ns, f, K, z["A"])
            print(f"\n{z['name']} (A {z['A']}, wf {z['wf']}), J {Jf}, K {K}, prec {d.get('prec')}, procs {d.get('procs')}, seconds {d.get('seconds')}; "
                  f"{fixed} of {len(f)} f entries beyond a double were rebuilt from the run log's 10 digits")
            print("| nu | \|F_nu/F_1\| | \|F_(nu+2)/F_nu\| | terms | last term / F_nu |\n|---|---|---|---|---|")
            for nu in range(1, 12, 2):
                print(f"| {nu} | {fm(S[J]['rel'][nu])} | {fm(S[J]['ratio'][nu])} | {S[J]['nterms'][nu]} | {fm(S[J]['last'][nu], 2) if nu > 1 else 0} |")
        if len(S) == 2:
            j = judge(S[750], S[1000])
            h = z["hier"]
            print(f"\n{z['name']}: |F_nu/F_1| at nu 3, 5, 7: J 750 {fm(S[750]['rel'][3])} {fm(S[750]['rel'][5])} {fm(S[750]['rel'][7])}; J 1000 "
                  f"{fm(S[1000]['rel'][3])} {fm(S[1000]['rel'][5])} {fm(S[1000]['rel'][7])}; hier (#1027) {h[0]:.3f} {h[1]:.3f} {h[2]:.3f}")
            print(f"  |F_7/F_5|: J 750 {fm(j['r75'][0])}, J 1000 {fm(j['r75'][1])}, hier {z['h75']:.3f}")
            print("  J agreement in |F_nu/F_1| (absolute): " + ", ".join(f"nu {nu}: {fm(j['agree'][nu])}" for nu in (3, 5, 7)))
            print(f"  last term <= {LAST_BAR:g} of F_nu at nu 3, 5, 7 at both J: {j['c1']}; J agree to {AGREE_BAR:g}: {j['c2']}  ->  converged: {j['conv']}")
            print(f"  READING {z['name']}: {j['reading']}")
            allj[z["name"]] = j["reading"]
    if allj:
        print("\nreadings: " + "; ".join(f"{k}: {v}" for k, v in allj.items()))'''
s = s[:a] + new_main + s[b:]
s = s.replace("import json\nimport os\nimport subprocess\nimport sys\n\nimport numpy as np\n", "import json\nimport os\nimport re\nimport subprocess\nimport sys\n\nimport mpmath as mp\nimport numpy as np\n", 1)
open(p, "w", encoding="utf-8").write(s)
