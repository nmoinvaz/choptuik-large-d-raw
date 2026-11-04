"""Planted-truth test of every candidate representation, through the same fit code (forms.py) as the real data.

FROZEN BEFORE THE FIRST RUN (2026-11-04).

Grid and noise: the 1214 cleaned real points D = 3.04375-67.77 (common.data()), each plant value plus Gaussian noise
of the point's own error (1e-15 to 1.2e-9), seed 1. The M48 thin points (4.25-8.2) get the plant plus noise of their
estimated error.

Plants (truth known exactly):
  P0  R(e), the README rational formula (stored coefficients), e = 1/n: poles only (D = -3.24, -11.0, and order 6 at
      D = 2); analytic at D = 3. Dinf = a0, Delta(3) = R(1).
  P7  R(e) + B sqrt((1 - e)(1 - e/e_s)), e_s = 1/n_s, n_s = -11 (square-root cut D in [-9, 3]), B = 0.5.
      Dinf = a0 + B, Delta(3) = R(1), n_s = -11.
  P8  the same with n_s = -8 (cut [-6, 3]). Dinf = a0 + B, Delta(3) = R(1), n_s = -8.
  Pz  data-like cut plant: Z-poly K = 28, n_s = -11 fitted to the real data (all D). Exactly a cut [-9, 3] with
      square-root ends, no poles. Dinf, Delta(3) its own values, n_s = -11.
  Pe  data-like pole plant: E-rat (8, 4) fitted to the real data on D >= 4, continued to D < 4 (accepted only if
      pole-free on D >= 3). Dinf = its value at e = 0.
      [Added after the first call, before any grading: Pe has a pole on 3 < D < 4, so by the rule above it is used on
      D >= 4 only, and the whole-range Z-* candidates are not run on it.]

Candidates and fit choices:
  Z-poly  polynomial in zeta(n_s): K in {24, 28, 32} x n_s in {-9, -11, -13} fixed, and K in {24, 28, 32} n_s free.
  Z-rat   rational in zeta(n_s), n_s free: (p, q) in {(8, 8), (10, 10)}.
  Z-log   polynomial in zeta(-11) plus (1 - zeta)^j ln(1 - zeta): K in {24, 28} x j-sets {1}, {2}, {1, 2}.
  E-rat   rational in e on D >= 4 (the README family): (p, q) in {(8, 2), (8, 4), (10, 4), (8, 8)}.
  N-poly  polynomial in 1/n on D >= 10: K in {16, 18, 20}  (reference for the held-out diagnostic).
  W-poly  polynomial in w1(n_s) on D >= 10: n_s in {-9, -11, -13} x K in {12, 14, 16}.
Splits: full; H1 fit D <= 45, held out D > 45; H2 fit D >= 3.1, held out D < 3.1; H3 fit without 4 < D < 8.25,
held out D = 5, 6, 8 and the M48 points. H2 only for forms that reach D < 3.1, H3 for forms that reach D = 4.

AMENDMENT before any zeta candidate was graded (the first P0 run, float64, is discarded): float64 is not adequate
for the whole-range zeta fits (cond 1e11-1e14, and the float64 basis alone gives chi2 ~ 1e3; cond_probe.py), so Z-poly,
Z-rat and Z-log now run in 256-bit arb (arbfit.py). Z-rat drops free n_s (60 s per fit): (p, q) in {(10, 10), (12, 12)}
x n_s in {-9, -11, -13}. Z-log: K in {24, 28} x j-sets {1}, {2}. Pz is regenerated with the arb fit. E-rat, N-poly and
W-poly stay in float64 (they reach max |r|/sigma ~ 4 on P0 there). Grading rules unchanged; G3 uses the free Z-poly
fits only.

Pass criteria (graded on the full fits):
  G1 Dinf: quoted value = centre of [min, max] over the candidate's fit choices, +- = half-range (a spread over fit
     choices). Pass if |centre - true| <= max(half-range, 1e-11).
  G2 Delta(3) (zeta forms only): same rule, floor 1e-6.
  G3 n_s (free-n_s fits): pass if the true n_s lies in [min, max] of the free fits widened by 0.5.
  Graded only where the plant is in the candidate's class: Z-* on P7, P8 (G3 only with n_s free), Pz; E-rat on P0,
  Pe; N-poly, W-poly on P0, Pe, Pz (G1 only). Elsewhere the same numbers are reported as 'info' (out of class: does
  the quoted spread still cover the truth?).
  G4 (reported): the full fit's max |r|/sigma and chi2/dof, and the held-out maxima.
  G5 the diagnostic: A = best H1 of N-poly / best H1 of W-poly (and of Z-poly), per plant and on the real data. Reading
     fixed in advance: the real data favour a cut only if their A is within 3x of the cut plants' (P7, Pz) and at least
     10x the pole plants' (P0, Pe).

    python3 planted.py [P0 P7 ...]     writes planted_<plant>.json
"""
import json, sys, time
import numpy as np
import common as C, forms as F
_J = json.load(open('/Users/nathan/Source/choptuik-large-d/solver/data/formula_coefficients.json'))   # README formula
A_ = np.array([float(v) for v in _J['a']]); B_ = np.r_[1.0, [float(v) for v in _J['b']]]

D, H, L, s, run = C.data(); TH = C.thin_m48()
R = lambda d: np.polyval(A_[::-1], C.eps(d)) / np.polyval(B_[::-1], C.eps(d))
sq = lambda d, ns: np.sqrt((1 - C.eps(d)) * (1 - ns * C.eps(d)))     # e/e_s = n_s e
BAMP = 0.5

CANDS = {
    'Z-poly': [(F.fit_zeta_poly_arb, K, dict(ns0=ns)) for K in (24, 28, 32) for ns in (-9.0, -11.0, -13.0)]
              + [(F.fit_zeta_poly_arb, K, dict(free=True)) for K in (24, 28, 32)],
    'Z-rat': [(F.fit_zeta_rat_arb, pq, dict(ns0=ns)) for pq in ((10, 10), (12, 12)) for ns in (-9.0, -11.0, -13.0)],
    'Z-log': [(F.fit_zeta_log_arb, (K, js), {}) for K in (24, 28) for js in ((1,), (2,))],
    'E-rat': [(F.fit_eps_rat, pq, {}) for pq in ((8, 2), (8, 4), (10, 4), (8, 8))],
    'N-poly': [(F.fit_n_poly, K, {}) for K in (16, 18, 20)],
    'W-poly': [(F.fit_w1_poly, K, dict(ns=ns)) for ns in (-9.0, -11.0, -13.0) for K in (12, 14, 16)],
}
INCLASS = {'Z-poly': ('P7', 'P8', 'Pz'), 'Z-rat': ('P7', 'P8', 'Pz'), 'Z-log': ('P7', 'P8', 'Pz'),
           'E-rat': ('P0', 'Pe'), 'N-poly': ('P0', 'Pe', 'Pz'), 'W-poly': ('P0', 'Pe', 'Pz')}

def plant(name):
    if name == 'P0': return R, dict(Dinf=A_[0], D3=float(R(np.array([3.0]))[0]), ns=None)
    if name in ('P7', 'P8'):
        ns = -11.0 if name == 'P7' else -8.0
        return (lambda d: R(d) + BAMP * sq(d, ns)), dict(Dinf=A_[0] + BAMP, D3=float(R(np.array([3.0]))[0]), ns=ns)
    if name == 'Pz':
        ev, info = F.fit_zeta_poly_arb(D, H, L, s, 28, ns0=-11.0)
        return (lambda d: (lambda hl: hl[0] + hl[1])(ev(d))), dict(Dinf=info['Dinf'], D3=info['D3'], ns=-11.0)
    if name == 'Pe':
        ev, info = F.fit_eps_rat(D, H, L, s, (8, 4))
        return ev, dict(Dinf=info['Dinf'], D3=None, ns=None, poles_D=list(map(str, info['poles_D'])), dmin=4.0)

def grade(vals, true, floor):
    lo, hi = min(vals), max(vals); c, h = (lo + hi) / 2, (hi - lo) / 2
    return dict(centre=c, half=h, off=c - true, ok=bool(abs(c - true) <= max(h, floor)))

def main():
    names = sys.argv[1:] or ['P0', 'P7', 'P8', 'Pz', 'Pe']
    rng = np.random.default_rng(1)
    for pn in names:
        T0 = time.time(); f, truth = plant(pn)
        dm = truth.get('dmin', 0.0); m = D >= dm - 1e-12; Dq, sq_ = D[m], s[m]
        y = f(Dq) + rng.normal(0, 1, len(Dq)) * sq_
        Hp = y.copy(); Lp = np.zeros(len(Dq))
        th = (TH[0], f(TH[0]) + rng.normal(0, 1, len(TH[0])) * TH[2], TH[2])
        out = dict(truth={k: v for k, v in truth.items()}, cands={})
        for cn, lst in CANDS.items():
            if dm > 0 and F.DMIN[lst[0][0]] < dm: continue
            rows = []
            for fn, ch, kw in lst:
                rows.append(dict(choice=str(ch), kw={k: v for k, v in kw.items()}, **F.evaluate(fn, Dq, Hp, Lp, sq_, ch, thin=th, **kw)))
            full = [r['full'] for r in rows if 'error' not in r['full']]
            g = dict(G1=grade([r['Dinf'] for r in full], truth['Dinf'], 1e-11))
            if cn.startswith('Z-') and truth.get('D3') is not None:
                g['G2'] = grade([r['D3'] for r in full], truth['D3'], 1e-6)
                fr = [r['full']['ns'] for r, (fn, ch, kw) in zip(rows, lst) if kw.get('free') and 'error' not in r['full']]
                if fr and truth.get('ns') is not None:
                    g['G3'] = dict(min=min(fr), max=max(fr), ok=bool(min(fr) - 0.5 <= truth['ns'] <= max(fr) + 0.5))
            g['graded'] = pn in INCLASS[cn]
            g['bestH1'] = min(r['H1']['max'] for r in rows if 'max' in r.get('H1', {}))
            if any('H2' in r and 'max' in r['H2'] for r in rows): g['bestH2'] = min(r['H2']['max'] for r in rows if 'max' in r.get('H2', {}))
            if any('H3' in r and 'max' in r['H3'] for r in rows):
                g['bestH3'] = min(r['H3']['max'] for r in rows if 'max' in r.get('H3', {}))
                g['bestH3thin'] = min(r['H3']['thin_max'] for r in rows if 'thin_max' in r.get('H3', {}))
                g['bestH3thinrs'] = min(r['H3']['thin_maxrs'] for r in rows if 'thin_maxrs' in r.get('H3', {}))
            g['best_full_maxrs'] = min(r['maxrs'] for r in full)
            out['cands'][cn] = dict(grade=g, rows=rows)
            tag = ('PASS' if all(v['ok'] for k, v in g.items() if k in ('G1', 'G2', 'G3')) else 'FAIL') if g['graded'] else 'info'
            ex = ''.join(f" {k} off {v['off']:+.1e} (+-{v['half']:.1e})" for k, v in g.items() if k in ('G1', 'G2'))
            if 'G3' in g: ex += f" G3 ns {g['G3']['min']:.2f}..{g['G3']['max']:.2f}"
            print(f"{pn} {cn:7s} {tag}:{ex} | best H1 {g['bestH1']:.1e}" + (f" H2 {g['bestH2']:.1e}" if 'bestH2' in g else '')
                  + (f" H3 {g['bestH3']:.1e} thin/sigma {g['bestH3thinrs']:.1e}" if 'bestH3' in g else '') + f" | full max|r|/s {g['best_full_maxrs']:.1e}"
                  + f"  ({time.time() - T0:.0f} s)", flush=True)
        json.dump(out, open(f'planted_{pn}.json', 'w'), indent=1, default=lambda o: str(o))

if __name__ == '__main__':
    main()
