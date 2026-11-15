# I871-mac: Theorem A(5)'s sets X_c and X_b stated exactly, and the zero's enclosure in the decimal box

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/871. Code:
`solver/proof/theorem_A_sets_M.py`, branch `wip/sa-871` on main 2d631290: the script at 2cfa4116, the text of
proof/A_lemmas_M.md (summary, §6, §7, §10) at 3a558c81.

`run_i871.sh <python> <root of the raw-data clone>` ran everything from `solver/proof/`, in under 10 s. `exits.txt`
has each run's command, its exit status and the status it must have: 4 checks exit 0 and 4 mutations exit 1. Each
run's log is `<name>.log`.

## The two sets at M = 5

- **X_b, the covering's ball.** Centre c = `I38-macm3/lemma6b1_runs_M5_cert/ray.json`'s `x`, the certificate's p̂ cut
  at 39 decimals. |p̂ − c| is 4.61×10⁻³⁹ in A, 8.49×10⁻⁴¹ in ω/ω∞, 8.83×10⁻³⁹ in B₃, 3.26×10⁻⁴⁰ in C₃, 1.82×10⁻³⁹ in B₅
  and 8.81×10⁻⁴⁰ in C₅. Radius: that of `arb(0, arb("1e-18"))`, which arb stores as a 30-bit number rounded up,
  10⁻¹⁸ + 2.193×10⁻²⁷, in every parameter.
- **X_c, the decimal box.** The chart image p(X) of X = [−10⁻¹⁸, 10⁻¹⁸]² × [−10⁻²⁶, 10⁻²⁶]² × [−10⁻²⁷, 10⁻²⁷]² around
  p̂ (the sub-box of the stored lemma 6a input, `I103-macm3/A_M2_6a_M5_sub1e-18.json`; the chart of
  `data/A_M2_box_M5_1e-10.json`). The certificate's Krawczyk sub-box is the arb ball with the same radii rounded up.

## Results

| check | result |
|---|---|
| (0) the Krawczyk test on the certificate's arb ball, rerun from the stored box file | K(X) ⊂ int X: yes, relative margins 1.000, 1.000, 0.980, 0.980, 0.932, 0.932 (the values of `I103-macm3/krawczyk_sub1e-18.log`); the ball contains the decimal box |
| (1) K(X) inside the decimal box | yes: \|K\| ≤ 6.08×10⁻²⁴ and 4.96×10⁻²⁴ against 10⁻¹⁸; 1.99×10⁻²⁸ (twice) against 10⁻²⁶; 6.80×10⁻²⁹ (twice) against 10⁻²⁷ |
| (2) the decimal box inside X_b | yes: slack 2.193×10⁻²⁷ in A and in ω/ω∞; 5.885×10⁻¹⁹, 9.536×10⁻¹⁹, 9.562×10⁻¹⁹, 9.918×10⁻¹⁹ in B₃, C₃, B₅, C₅ |
| for reference: the certificate's arb ball against X_b | passes X_b's edge by 4.613×10⁻³⁹ in A and 8.493×10⁻⁴¹ in ω/ω∞ |
| the zero's enclosure p(K(X)) | radius 6.08×10⁻²⁴ in A, 4.96×10⁻²⁴ in ω/ω∞, at most 2.2×10⁻²⁴ in the inner parameters |
| verdict | HOLD |

So existence and uniqueness of the zero hold on the decimal box, and (H2) holds for it. The inclusion rests on arb's
rounding of the covering's radius: its slack in A is the rounding excess 2.193×10⁻²⁷ less 4.6×10⁻³⁹.

At M = 3 the hull of the certificate's box (half-widths 1.00×10⁻¹⁰, 1.00×10⁻¹⁰, 3.87×10⁻¹¹, 2.51×10⁻¹²) lies in
X_b = c ± 1.1×10⁻⁹ with slack 9.997×10⁻¹⁰; the centres differ by 2.66×10⁻¹³ in A.

**Mutations** (each must exit 1, and does).

| mutation | what fires |
|---|---|
| `decimal`: X_b's radius replaced by the exact decimal 10⁻¹⁸ | (2): slack −4.613×10⁻³⁹ in A, −8.493×10⁻⁴¹ in ω/ω∞ |
| `centre`: X_b's centre moved by twice its half-width in A | (2): slack −2.000×10⁻¹⁸ (M = 5), −1.200×10⁻⁹ (M = 3) |
| `kbox`: the decimal half-widths replaced by half of \|K\|'s bounds | (1): K(X) outside |

The first run of the driver expected the M = 3 centre mutation to fire with a move of 10⁻²⁰, which cannot break an
inclusion whose slack is 10⁻⁹. The mutation now moves by twice the box's half-width, and every run was repeated.

## Recommended tasks

1. **An X_c that does not rest on the rounding.** What: state Theorem A(5) on a decimal box strictly inside X_b, for
   example X = ±(9×10⁻¹⁹, 10⁻²⁶, 10⁻²⁷), and rerun `theorem_A_sets_M.py` with that sub-box. Why: K(X) lies within
   6.1×10⁻²⁴ of p̂, so any box between K(X) and X_b serves, and the present inclusion has a slack of 2.19×10⁻²⁷ that
   comes from how arb stores a radius. Lemma 6a's state box covers the larger sub-box already. Acceptance: the script
   reports (2) with a slack near 10⁻¹⁹ and still HOLD with the covering's radius taken as the decimal 10⁻¹⁸. Depends
   on: #871.

The README and PROOF.md do not state Theorem A(5)'s box (they give the interval of ω/ω∞), so they need no change.
