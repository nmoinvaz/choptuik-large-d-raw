# I894-mac: an independent review of the floor of lemma LC's Lipschitz matrix

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10, every run under a time cap (580 s for the runs of `b8m_lc.py`). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/894. Review note: `proof/B_LC_floor_review.md`; script:
`solver/proof/review_894/rv_floor.py`; branch `wip/sa-894` on main dbaf7af3, at f72cbd35. The reviewer did not write the floor
(#891) or any of `b8m_lc.py`.

`exits.txt` has each run's command, its exit status and the status it must have. Files:

- `liprep/`: the outputs of `b8m_lc_liprep.py --out` and of its `--mutate=nofloor`: `lip.json` (floor 10⁻⁵⁰),
  `lip_dA.json` (centre moved by 10⁻¹⁷), `lip_nofloor.json`, `lip_nofloor_dA.json`, and each run's `lc*.log` (the
  record) and `lc*.out`; `liprep.txt`, `liprep_nofloor.txt` are the script's own output.
- `cap/`: the reviewer's mutation, two runs: `lip_cap.json`, `lip_cap_dA.json`, `lc_cap*.log`, `lc_cap*.out`;
  `cap_runs.txt`.
- `rv_floor.txt` (K1 to K5 on the real matrices), `rv_floor_mut_cap.txt` (K1 on the mutated one),
  `liprep_on_cap.txt` and `lipcheck_on_cap.txt` (the author's checks on the mutated matrices).

## Verdict

The floor is sound and θ = 0.7355 stays certified. No finding changes a number or a verdict. One finding is about
check coverage: none of the author's checks can tell a raised entry from a lowered one (F1 of the note).

## Results

| check | criterion, written before the runs | result |
|---|---|---|
| R1, by reading | the flooring line can only raise an entry; its comparison is decided; the floored matrix is the one certified and saved | holds |
| R2 = K1, floored against unfloored at the same centre | no entry lowered; equal in every digit above the floor; the floor elsewhere; 1204 at the floor (1184 below 10⁻⁶⁰, 20 between 10⁻⁶⁰ and 10⁻⁵⁰); smallest above 4.9×10⁻⁵⁰ | 0 lowered; 396 above, all equal; 1204 written as the floor (1184 and 20); smallest above 4.912×10⁻⁵⁰, largest below 4.852×10⁻⁵³ |
| R3 = K2, the row sums in exact rational arithmetic | the floored entries add at most 2.4×10⁻⁴⁸; θ = 0.735467756408 with and without the floor | 2.339×10⁻⁴⁸ with the certificate's weights; θ 0.735467756408 both, rising by 5.5×10⁻⁵⁰; with the reviewer's own weights θ = 0.705132216712 both |
| R4 = K3, centres 10⁻¹⁷ apart | the same entries at the floor; those above it within 5.3×10⁻¹¹ | the same 1204; at most 5.29×10⁻¹¹ (at `der/S/Nb<-val/b/N0`), 37 above 10⁻¹² |
| R5 = K4, K5 | the saved fields say what the matrix is; the stored matrix equals the rerun | floor 10⁻⁵⁰, floored 1204 (recounted 1204), eta 10⁻⁶, the note; stored `b8m_lc_lip.json`: 0 of 1600 entries differ; the stored record `b8m_lc_K4.log` equals the rerun's in every number but the run times |
| R6, the author's check and control | `b8m_lc_liprep.py` exits 0; `--mutate=nofloor` exits 1 with 636 entries differing | exit 0 (0 differ, largest 5.3×10⁻¹¹); exit 1 (636 differ, largest 0.27) |
| R7, the reviewer's mutation `cap`: every entry written as the floor | K1 must fail on it, exit 3 | exit 3: 396 entries lowered, the largest from 1.0 to 10⁻⁵⁰ |

**What the author's checks say about the mutated matrices** (reported as a finding either way):

| check | result |
|---|---|
| the certificate's command on the mutated code | exit 0, "1600 of 1600 entries are at the floor", "certified theta = 0.0000 (< 1: True)" |
| `b8m_lc_liprep.py --compare` on the two mutated runs | PASS, exit 0 (0 entries differ, θ = 0.0000 and 0.0000) |
| `b8m_lc.py --lipcheck` on the mutated matrix | exit 0, θ = 0.0000 |

## Findings (full text in the note)

1. F1, check coverage: no author's check can tell a raised entry from a lowered one, and `check_numbers.py` has no
   check on θ = 0.7355. The stored matrix is not affected.
2. F2, text: the saved note names rounding noise as the cause; 20 of the 1204 floored entries are real bounds.
3. F3, observation: the floor lies a factor 5 below the smallest real entry above it; the populations are three
   decades apart at this box.
4. F4, statement precision: "at most 2.4×10⁻⁴⁸ to a weighted row sum" holds for the certificate's weights.
5. F5, observation: the saved floor is the double 1e-50, above the decimal by 7.6×10⁻¹⁸ relative.

## Recommended tasks

1. **A check that tells a floor from a cap.** What: in `b8m_lc_liprep.py`, compare the floored run with the
   unfloored one entry by entry (no entry lowered, equal above the floor, the floor elsewhere), as
   `review_894/rv_floor.py` K1 does, and keep the reviewer's `cap` mutation as its control. Why: F1. Acceptance:
   the check passes on main and fails (non-zero exit) on the `cap` mutation. Depends on: #894.
2. **θ = 0.7355 among the checked numbers.** What: a `check_numbers.py` entry for θ, from `b8m_lc_K4.log`'s
   `lip.theta`. Why: F1; the number is quoted five times in B_chain.md and is tied to no file. Acceptance: the
   selftest rejects a shifted value. Depends on: #894.
3. **The note's wording** (F2) **and one phrase in §13.4** (F4). What: "An entry at or below floor is written as
   floor, whatever its cause", and "with the weights of the certificate". Acceptance: `check_numbers.py --selftest`
   passes; the stored matrix's entries do not change (K5). Depends on: #894.
