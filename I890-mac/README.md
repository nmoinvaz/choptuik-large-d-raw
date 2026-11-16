# I890-mac: the stored outputs of the B8 chain regenerated with the current code, and the comparisons

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/890. Code: branch `wip/sa-890` on main
e53b8bc8, which holds #885, #887 and #891. The regenerated files are in that branch, in `solver/proof/`. This folder
holds the records of the runs and the comparisons.

## What ran

`solver/proof/b8_chain_regen.sh`, new: the commands of proof/B8_constants.md §13 and proof/B_chain.md §11 from
`b8m_atoms.py` on, without the `b7_adjoint.py` runs. It writes 35 outputs under their stored names and in their stored
layouts, with every appended log emptied first. It took 20 min. `regen.txt` has the first run's exit statuses, in the
script's earlier format, which expected exit 1 from the three scans that do not close. `b8m_scan.py` exits 0 there,
so the script now expects 0 everywhere. `regen_second.txt` is the second run of the committed script: every command
exits 0.

Five of the stored files came from commands that the notes did not state, and their layouts gave them:

| file | command |
|---|---|
| `b8m_scan_K4_box.log`, fifth record | the scan's list of ln n₀ ends with 58, which does not close |
| `b8m_atoms_K4.log` | `b8m_atoms.py 4 0 0`, then `b8m_atoms.py 4 2e-6 2e-6` |
| `b8m_scan_K4_d0.log` | `b8m_scan.py 4 73.89 --d0=...` for 10⁵ to 10⁹, of which 10⁸ and 10⁹ do not close |
| `b8m_scan_K4_fixedZ.log` | `b8m_scan.py 4 90 --kappa1=0.7308324141810887` |
| `b8m_h8_K4_L104.68_k0.85.log` | `b8m_h8.py 4 104.68 --log=b8m_scan_K4_k0.85.log --kappa1=0.85` |

Each reproduces its stored file to 1.7×10⁻¹¹ or better, which is the check that the command is the right one.

## Three comparisons (`compare_i890.py <new> <old>`)

| file | compares | result |
|---|---|---|
| `compare_stored.txt` | the regenerated files with the ones stored before | below |
| `compare_previous_runs.txt` | with the outputs of `I887-mac/`, and of `I891-mac/` for lemma LC's three files | 0 in every number of all 25 files |
| `compare_second.txt` | the second run with the committed files | 0 in every number of all 35 files; 11 files differ in their wall times only |

In `compare_previous_runs.txt` the line counts differ where the stored layout has an `exit` line, a second run or
the last lines of several runs, and `b8m_lc_numcheck_mut.log` pairs lines of different runs for that reason. That
file is byte for byte the stored one.

## Regenerated against stored before

| files | difference |
|---|---|
| 12 files: `b5_jump*.log`, `b5_threshold.log`, `b7_ift.log`, `b7_ift_mutJD.log`, `b8m_atoms_K4.log`, `b8m_lc_lipcheck.log`, `b8m_lc_numcheck_mut.log`, `b8m_lc_numcheck_n1e3.log`, `b8m_lcj.json`, `b8m_lcj.log` | none, byte for byte |
| `b5_jump*.json`, `b7_ift.json` | at most 9.8×10⁻¹⁵ |
| the four `b8m_h8_*.log` | at most 5.3×10⁻¹⁶, in the record line |
| `b8m_lc_K4.log`, `.out` | at most 3.9×10⁻¹⁵; two new fields and one new line for the floor |
| `b8m_scan_K4_d0*.log`, `_fixedZ.log`, `_k0.85.log` | at most 1.7×10⁻¹¹; the field `d0` is new in the last two |
| `b8m_scan_K4_box.log`, `.out` | the field `d0` is new; at ln n₀ = 62, 67 iterations against 70, h within 4.2×10⁻⁷, closes; the other records within 5.9×10⁻¹⁶ |
| `b8m_lc_lip.json` | 1204 entries at the floor 10⁻⁵⁰, where the old values were at most 4.9×10⁻⁵³; the 396 above it within 4.5×10⁻¹⁶; four new fields |
| `b8m_lc_K4_mut_rho2L.log`, `.out` | 4×10⁻³ in the last relative change: the record of a mutated certificate, still caught |
| `b8m_lcj_mutations.log` | 4.1×10⁻⁷ in the weights that the `Om` mutation prints; θ = 2.8342×10² as before, caught |
| `b7_ift_d0_0.log`, `b7_ift_d0_1e6.log` | C_E = e^76.9145 and e^76.9163 against e^76.9143 and e^76.9161; C₇ = 2.8233×10²⁹ and 2.8286×10²⁹ against 2.8228 and 2.8280; n₀ = e^89.75 in all |

The two `b7_ift_d0` logs were last written on 2026-10-23, before the fix F6 of proof/P2b_review.md changed C_E, so
their difference is that fix and not the precision.

## Verdicts

θ = 0.7355 (`b8m_lc_lipcheck.log`), n₀ = e^89.75 and C₇ = 2.8959×10²⁹ (`b7_ift.log`), lemma J's θ = 0.17593
(`b8m_lcj.log`), and the six mutations are caught. `review_p2/p2_perron.py` passes on the regenerated matrix
(θ ≤ 0.7356).

## Left as stored

| file | why | rerun here |
|---|---|---|
| `b8m_numcheck_n1e3.log` and its mutation logs | a numerical check in double precision, whose sampled points depend on the machine | `b8m_numcheck_n1e3.new.log`: ALL CHECKS OK with the regenerated scan log, 10 lines differ from the stored log |
| `b8m_h8_centre.log` | its second half is a traceback with the paths of the machine that made it | `b8m_h8_centre.new.log`: exit 0, its five lines equal the stored ones byte for byte; `b8m_h8_centre_mut.new.log`: exit 1 with the same error |
| `b8m_identities.log` | | `b8m_identities.new.log`: equal to the stored log |
| the `b7_adjoint.py` files, `b5_label*`, `b5_bounds*` | their scripts and inputs did not change | |
| the `*_preP2b*` files | snapshots of the state before P2b | |
