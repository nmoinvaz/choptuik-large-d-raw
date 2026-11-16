# I891-mac: lemma LC's Lipschitz matrix with a floor, compared between two runs with centres 10⁻¹⁷ apart

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/891. Code: branch `wip/sa-891`, on top
of #887. `b8m_lc.lipschitz` writes every entry of the matrix below `--lipfloor` (10⁻⁵⁰) as the floor, and the saved
file carries `floor`, `floored`, `eta` and a note.

## Why a floor and not zeros

A secant (M(η) − M(0))/η of a bound that does not depend on the perturbed input is rounding noise over η, at most
2.3×10⁻⁶⁹ (`I885-mac/`). The two evaluations bound such a slope by that number, and they do not prove it is zero. 44
more entries are a real bound of at most 6×10⁻⁶³ plus noise, and they differ between runs by 10⁻⁷ whatever is done to
the pure noise. Raising an entry keeps it an upper bound, so a floor needs no further argument and gives the same
number in every run.

## The check

`python3 b8m_lc_liprep.py --out=<this folder>` ran `b8m_lc.py 4 73.89 --rA=2e-6 --rW=2e-6 --lip` twice, with the
centre A\* of the box as it is (`lip.json`, `lc.log`, `lc.out`) and moved by 10⁻¹⁷ (`lip_dA.json`, `lc_dA.*`), and
compared the two matrices. `--mutate=nofloor` did the same with `--lipfloor=0` (`lip_nofloor*.json`,
`lc_nofloor*.*`). Outputs: `liprep.txt`, `liprep_nofloor.txt`.

| run | entries that differ by more than 10⁻⁹ | largest relative difference | θ of the two | verdict |
|---|---|---|---|---|
| with the floor | 0 of 1600 | 5.3×10⁻¹¹ | 0.7355, 0.7355 | PASS, exit 0 |
| `--mutate=nofloor` | 636 | 0.27 | 0.7355, 0.7355 | FAIL, exit 1, as it must |
| `--compare` of the stored file and `I885-mac/b8m_lc_lip.json` | 515 | 0.27 | 0.7355, 0.7355 | FAIL, exit 1 |

The 5.3×10⁻¹¹ is not noise. It is the change of the closure's constant h_β in the band N0 (21.4765547506 against
21.4765547495 for P(h)), which every entry of its row and column carries. 37 entries differ by more than 10⁻¹², and
all of them are above the floor.

## What the floor costs

| | value |
|---|---|
| entries at the floor | 1204 of 1600, the same 1204 in both runs |
| of them below 10⁻⁶⁰ without the floor | 1184 |
| of them real bounds between 10⁻⁶⁰ and 10⁻⁵⁰ | 20 |
| smallest entry above the floor | 4.9×10⁻⁵⁰ |
| entries above the floor, with and without it | equal in every digit |
| what the floored entries add to a weighted row sum | at most 2.4×10⁻⁴⁸ |
| θ, with and without the floor | 0.735467756408 both |

The record of the run as written (`lc.log`) equals the stored `b8m_lc_K4.log` to 3.9×10⁻¹⁵ in every number, apart
from the two new fields `lip.floor` and `lip.floored`.
