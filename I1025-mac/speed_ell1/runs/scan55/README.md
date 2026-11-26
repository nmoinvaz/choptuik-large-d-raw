# scan55: d18_secant.py scan checked against d18_hybsign.py on the k_c 55 state (#1025)

Machine: the coordinator's Mac (Apple M5), venv-1025dd, one BLAS and one rayon thread per process, nice 10, two
processes side by side, beside other jobs. Code: d18_secant.py at wip/ell1-speed 92b9bf53 (blob eb1396ad). Input: I1025-mac/out/
l1kc55F1025.jsonl (0fb77df8) and sol_l1kc55F1025_D18.125000.npy (88ccda5c), D 18.125, lambda 1.77.

Bars, written before the run: --mm=cs equals d18_hybsign.py's record (../repro/repro_177.jsonl) bit for bit; --mm=fast
has the same hybrid sign with ln|det| within 1e-8, and is not bit-identical (the comparison's control).

| scan | hybrid sign | ln|det| | minus d18_hybsign's | float64 sign | seconds [matrix, dd block 12, det] |
|---|---|---|---|---|---|
| --mm=cs | +1 | -1617.4278109138 | 0 (bit for bit: PASS) | -1 (equal) | 331 [108, 220, 3] |
| --mm=fast | +1 | -1617.4273560115 | +4.549e-4 | +1 (differs) | 267 [22, 242, 3] |

The cs bar passes and the control fires (fast is not bit-identical). **The fast bar of 1e-8 FAILED as written.** The cause
is known: SPEED_ELL1.md ("Real refinements and the float64 floor of the root") measured this same difference, 4.5e-4 at
1.77, between the two codes' float64 blocks 0-11 (equal to 1e-14 per block), and the 1.4e-6 floor of the root it sets
at k_c 55 (about 1.5e-7 at k_c 103). The 1e-8 bar came from the k_c 31 check and was wrong for k_c 55; the coordinator
set it without reading that section. A fast scan's sign can differ from the old one's only within that floor of a
root, far inside a scan grid of 0.01-0.02. The float64-only sign (block 12 in float64) is not used by any reading;
its block 12 is wrong by 1.5e-10 in both codes.
