# I451-macm3: D 58.01, M 48: #266's double-double R2 state against its quad-double polish, component by component (a STAND-IN for #271's rerun)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon), the worktree ../choptuik-large-d-i271 at 408b4d6. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/451 (was #288).
Raw output is not committed here while the raw repository's rewrite pause lasts.

**This is a stand-in, as the coordinator wrote (21:07 UTC).** The issue asks for #271's rerun state at D 58.01, which gamma_dd.py did not save. This run compares #266's own two D 58 states instead: the R2 double-double state
(I266-mac/states/up12_D58.0060_M48_r2.npz) and its quad-double polish (up12_D58.0060_M48_r2_qd.npz), sha256 in state_sha256.txt. It answers the question for #266's R2 state, not for #271's. #271's record gave Delta(48) - Delta_qd = -1.875e-18 and a Newton step of +2.0e-18;
the issue stays open after the summary until gamma_dd.py has --save_state.

Command (run.sh, caffeinate -is, nice 10, one thread), #266's analyze:
python3 -u hp/gamma_m48_gap.py analyze <raw>/I451-macm3/analyze_D58.jsonl <raw>/I266-mac/states/up12_D58.0060_M48_r2.npz <raw>/I266-mac/states/up12_D58.0060_M48_r2_qd.npz --w=24 --threads=1 --lam

Written before the run. Report: the distance of the dd state from the quad-double one in Delta against 1.9e-18 (the issue's number), and the direction that carries it (the weak singular directions and their harmonic content, as #266's table at D 50). #266's table for D 58 already has: R2 dd state linearised dDelta -4.9e-18, qd polish -7.5e-19; Delta(48) - Delta(32) -1.447e-18 for the dd state.
If analyze refuses a four-part state as B, that is reported, not worked around.

## Results

Exit 0 (21:08:05 to 21:18:06 UTC; 10 min). Log analyze_D58.log, record analyze_D58.jsonl. A = R2 double-double state, B = its quad-double polish, one solver (B's plan, 13 Taylor steps both):
  Delta(A) 1.81537990111591269521805710667, Delta(B) 1.81537990111591269548046122778: Delta(A) - Delta(B) = -2.624e-19. |F| dd: A 1.39e-23, B 1.29e-23; in qd A 1.08e-23, B 3.97e-24. Linearised Delta correction: A -3.544e-18, B -5.586e-19.
  d = A - B: |d|_2 2.639e-11, Delta component -2.624e-19, 5.5e-13 of |d| outside the 24 weakest directions. Newton step at A against -d: cosine -0.172, |dz_A|/|d| 4.08 (at D 50 the cosine was 1 - 1e-13).
  d in the weakest directions: coefficients +2.234e-11 and +1.404e-11 on the pair 0, 1 (sigma 1.97e-22, the p1 harmonic 13), +2.429e-13 and +6.006e-13 on the pair 2, 3 (sigma 1.89e-20, harmonic 11); p1 harmonic amplitudes of d: k = 13 5.3e-12, 11 7.3e-13, 9 2.7e-14, 7 1.0e-15.
  lam at B 2.0455297614775274, at A 2.045529761477751: lam(A) - lam(B) = +2.234e-13.
