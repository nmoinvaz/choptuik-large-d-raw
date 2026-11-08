# I126-mac: EEG's large-D NNLO (printed and corrected) against the finite-D solutions, D 15-215

Machine mac (Apple M5), subagent of the coordinator. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/126.
Code: `solver/inner_pert/nnlo_vs_solution.py` of the main repository (branch wip/i126). Python: extract with
/Users/nathan/Source/venv-anm/bin/python (its hpkernel has `Solver.residual_q`), compare and planted with
/Users/nathan/venv-qd/bin/python (sympy). At most 2 processes, nice -n 10.

## What is compared

EEG's fields f, Omega, Pi, Psi (arXiv:2611.07007v1, supplement (S35)-(S51)), evaluated with beta~ = Pi(tau, 0)/sqrt(eps)
of each state (S34), eps = 1/(D - 1), against the state's own f = c, Omega = (n - 1)(a^2 - 1)/x^2,
Pi = (p - m)/(sqrt2 x), Psi = (p + m)/(sqrt2 x^2) (n = D - 2; notes/SECOND_ORDER.md section 1), on x = 0, 0.01, ..., 1
and the state's tau grid (32 points per half period). Models: LO, NLO (S40)-(S43), NNLO as printed (S44)-(S51), NNLO
corrected (second_order_eeg.py, check D), and the control NNLO corrected with Pi_3 x 1.01.

States: the double-double states of hp/data/states (main repository) for D 15-60, the full-system quad-double state
T81/conv_pin5_D73.0000_D73.000000.npz, and the held-on-fit chain T138-win2/chain (D 80-170) and chain_o (D 180-215);
for the spread between chains at equal D, T140-win/chain_d6 and chain_d10 at D 100 and 150, I13-win/chain_d6 and
chain_d10 at D 180.

## Acceptance criteria (written 2026-11-08 15:50 UTC, before the comparison was run on any real state)

R(D) is the maximal residual max |F_sol - F_model| over the grid (absolute). Its exponent p is fitted as
ln R = a + p ln eps + b eps by least squares over the states with D >= 40 (the main fit); the fit over D >= 20 and the
local exponents between neighbouring D are reported too.

Expected exponents (the first omitted, or first wrong, order of each model; Pi and Psi carry the overall sqrt(eps)):

| model | f | Omega | Pi | Psi |
|---|---|---|---|---|
| LO | 2 | 2 | 1.5 | 2.5 |
| NLO | 3 | 3 | 2.5 | 3.5 |
| NNLO printed | 3 | 3 | 2.5 | 3.5 |
| NNLO corrected | 4 | 4 | 3.5 | 3.5 |

- **C1 (corrected NNLO).** Each field's fitted p within 0.25 of the table and farther than 0.5 from one order lower.
- **C2 (printed NNLO).** The same against its row. If it fails, the measured exponents are reported.
- **C3 (LO and NLO, pipeline checks).** The same against their rows.
- **C4 (control, `--mutate=pi3x1.01`).** Pi_3 scaled by 1.01 (in Pi and in Omega_3 = 2 beta~ Pi_3 + ...; f_3 unchanged)
  must make C1 fail for Pi and Omega and leave it passing for f and Psi.
- **C5 (planted truth, run first).** Each state's fields replaced by the corrected NNLO of its own beta~ plus
  (1 + 4 eps + 20 eps^2) eps^p g with known shapes g (Pi's vanishing at x = 0), p = 4, 4, 3.5, 3.5 for f, Omega, Pi,
  Psi, through the same code: P1, the corrected model recovers each p within 0.1; P2, the printed model shows its
  error, p within 0.25 of 3, 3, 2.5 for f, Omega, Pi; with `--plant_pi=3`, Pi's fit returns 3 within 0.1; with the
  mutation, Pi's and Omega's fits differ from the plant by more than 0.25.
- **C6 (precision floor).** At each D the state's own field error (continuity of centre series and horizon series
  against the nodes, the horizon block's residual in quad-double, and the spread between chains at equal D) must be
  below 1% of the corrected NNLO's residual R(D). A D that fails is dropped from the fit and reported.

Note on the issue's wording: #126 says the corrected NNLO's residual should fall like eps^3 (Omega, f) and eps^(5/2) (Pi).
Those are the orders of the printed NNLO's first wrong terms. For the absolute residual the corrected one should fall
one order faster (table above). Measured with respect to the leading term, which is O(eps) for f - 1 and Omega and
O(sqrt eps) for Pi, the corrected residual is O(eps^3) for all three. Both readings are reported.

Fig. 5's measure: the relative rms deviation rms(F_sol - F_model)/rms(F_sol) over the (tau, x) grid (for f also
relative to rms(1 - f_sol)), printed, corrected, and the change printed - corrected, at each D.

## Results (2026-11-08, written after the runs)

Write-up: notes/SECOND_ORDER.md 1.1 of the main repository. Exits in exits.txt (the last block is the final code).

| criterion | verdict |
|---|---|
| C1 corrected NNLO: p = 3.971, 3.967, 3.442, 3.473 (f, Omega, Pi, Psi) | pass |
| C2 printed NNLO: p = 3.044, 2.986, 2.484, 3.473 | pass |
| C3 LO 1.986, 1.982, 1.493, 2.490; NLO 2.957, 2.975, 2.484, 3.473 | pass |
| C4 Pi_3 x 1.01: Pi 3.386, Omega 3.942 (within 0.25 of 3.5, 4) | FAIL, the control did not fire |
| C5 planted: recovers 4.008, 4.006, 3.491, 3.492; plant_pi=3 gives 2.991; mutation breaks the plant | pass |
| C6 floors at most 1e-6 of R; chain spread 2.7% and 6.8% of R at D 150 and 180 | D 150, 180 left the fit |

C4's cause: the true eps^(7/2) term's coefficient is about 30 times Pi_3's, so 1% of Pi_3 is only 2-7% of R over D
40-215. planted_big_mut (plant 1000 times larger, as large as the real residual) stays silent the same way. The test
resolves Pi_3 x 1.05 (Pi 3.22) and x 1.2 (Pi 2.94, Omega 3.63); compare_mut1.*.log.

## Files

- extract.cmd, extract.log: fields of every state (fields/, fields_t140_d6/, fields_t140_d10/: one npz per state with
  D, Delta, xs, f, Om, Pi, Psi on (x, tau) and the continuity diagnostics in info).
- planted.cmd: planted.log/json, planted_pi3.*, planted_mut.*; control_scan.cmd: compare_mut1.02-1.5.*,
  planted_big_mut.*, compare_dmax140.*, compare_dmin73.*.
- compare.cmd: compare.log/json (main run with the spread), compare_mut.* (C4), figs.log/json.
- figs.cmd: figs.log/json alone (Figs. 4-5 measures, exact, Eq. (16) and D = infinity profiles, centre profiles).
