# I746-rpi5: the misfit's profile over M on #718's ring records

Machine: rpi5 (Raspberry Pi 5, aarch64), one process under `nice -n 10`, 1.1 s and 34 MB per run, python 3.13, standard
library only.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/746

Code: `solver/inner_amp/misfit_profile_746.py` at f464eed4 of branch `wip/i746` of nmoinvaz/choptuik-large-d. The
criterion is frozen in `notes/PADE_FAR_END.md` §17 at a4854315, before the script existed and before any plant's χ at 20
or 21 terms was read. Input: `../I718-mac/` (`ring.jsonl`, `ring.json`, `control.json`) of this repository at 9d4b8d1d,
read-only. Records only, no new plant.

```
git clone https://github.com/nmoinvaz/choptuik-large-d-raw ../choptuik-large-d-raw
python3 solver/inner_amp/misfit_profile_746.py ../choptuik-large-d-raw/I718-mac --out ../choptuik-large-d-raw/I746-rpi5
python3 solver/inner_amp/misfit_profile_746.py ../choptuik-large-d-raw/I718-mac --mutate=scale_chi     # also :20, :22, drop_node
```

## Files

- `profile.log`, `profile.json`, `profile.time`: the run (controls, both maps, the counts, the post-freeze analysis).
- `mutate_scale_chi.log`, `mutate_scale_chi_20.log`, `mutate_scale_chi_22.log`, `mutate_drop_node.log`: the mutations.

## The criterion (frozen, §17.2)

ρ_M = χ_M / χ_M(real) at the same node, in zk/chord. (d′): 1/5 ≤ ρ_M ≤ 5 for M = 20, 21, 22 with the zero held at ZLOC
(`twin["kstar/chord"]`). (d″): the same with the plant's own located zero (`reloc`). P′ = (a), (c′), (d′) and P″ = (a),
(c″), (d″) at 0.99, 1.00 and 1.01, with #718's location rule. A plant that passes at ω∞ and has no record at another
node is unknown, as is a group or position whose best plant is.

## Controls

| check | result |
|---|---|
| records | 5967 plant records (303, 5392, 272 at 0.99, 1.00, 1.01), no duplicate (id, wf), 42 positions, 252 position-groups |
| counts at ω∞ | (a) 3477, (c′) 5064, (a) + (c′) 3401, (a) + (c″) 3433, as §16.4 |
| R-b | stored (a), (c′), (c″) and the ratios recomputed from the stored χ₂₂, M_min and the real χ₂₂: 0 of 5967 differ |
| R-a | with (d) off: `ring.json`'s pass, hit plant and `n_wf1` for every position, group and criterion, and its passing, edge, candidates and located lists, reproduced; no unknown group or position |
| J+ | ρ_M = 1 at every node, held and relocated; χ(real, ω∞) = 4744.8, 4359.1, 401.8 (§15.5: 4745, 4359, 402); 0.99: 4239.9, 4266.1, 411.2; 1.01: 5842.5, 5649.1, 427.5 |
| edge | planted ρ at F(1 ∓ 10⁻⁹), (1/F)(1 ± 10⁻⁹), 10, 1/10 and 1, for each M: inside passes, outside fails |
| `--mutate=scale_chi`, `:20`, `:22` | J+ (ρ = 10 at that M) and the edge check fail, exit 1 |
| `--mutate=drop_node` | R-a fails, exit 1 |

R-a shares only the records with #718's code. One amendment, made after the controls first ran and before any verdict
(§17.2): R-a's "no unknown status" is read at the level of groups and positions, since a plant after a group's hit was
never run at the other nodes (6251 plant statuses over the two criteria), so plant-level unknowns are expected with
(d) off. The gate stopped
that run, so no profile was printed.

## The verdict

|  | #718 passes | pass | unknown | fail | at \|Q\| ≥ 2.48: fail, unknown | candidates |
|---|---|---|---|---|---|---|
| P′, held | 34 | 0 | 22 | 12 | 12, 22 | none |
| P″, relocated | 37 | 24 | 12 | 1 | 0, 11 | none |

- P′ fails 12 positions at \|Q\| = 2.48–2.86: (−1,+2), (−1,+3), (0,+1), (0,+2), (0,+3), (+1,−1), (+1,0), (+1,+1), (+1,+2),
  (+2,−2), (+2,−1), (+2,0). At each, no plant passes (a), (c′) and (d′) at ω∞ (0 of 6 to 121 plants), so the failure is
  exact. The 22 unknown are at \|Q\| ≥ 2.86, each with plants that pass at ω∞ and no record at another node.
- P″ fails (0,−1) (\|Q\| 2.25, where #718's (c″) passed 2 of 6 groups; 0 of 4 plants pass (d″) at ω∞). No position at
  \|Q\| ≥ 2.48 fails. The 12 unknown are (0,−2), (+2,−1), (+2,+4), (+3,−2), (+3,−1), (+3,0), (+3,+1), (+3,+2), (+3,+3),
  (+4,+1), (+4,+2), (+4,+3). 11 of the 24 passing positions touch the lattice edge, (−1,+2) to (−1,+4), (0,+4),
  (+1,+4), (+2,−2), (+3,+4), (+4,−2), (+4,−1), (+4,0) and (+4,+4).
- No candidate in either variant: no position passes with four failing lattice neighbours. So nothing is located, and
  no stage 2 is called for.

## The profile's shape, context (reported, not judged)

The shape ratios σ₂₀ = ρ₂₀/ρ₂₂ and σ₂₁ = ρ₂₁/ρ₂₂ are χ₂₀/χ₂₂ and χ₂₁/χ₂₂ of a plant in units of the real series' (11.8 and
10.8 at ω∞), over the plants that pass (a) and (c′) (held) or (c″) (relocated) at ω∞.

| \|Q\| band | positions | held σ₂₀ | held σ₂₁ | relocated σ₂₀ | relocated σ₂₁ |
|---|---|---|---|---|---|
| 1.9–2.4 | 3–4 | 32–46 | 2.3–2.8 | 0.80–0.91 | 0.79–0.87 |
| 2.4–2.8 | 9 | 24–39 | 2.0–2.6 | 0.75–0.87 | 0.75–0.88 |
| 2.8–3.2 | 15 | 16–27 | 1.6–2.1 | 0.67–0.81 | 0.67–0.80 |
| 3.2–3.8 | 10 | 12.5–19.5 | 1.4–1.8 | 0.67–0.76 | 0.67–0.74 |

- Held, the shape is a function of position: at a fixed position, group, α and phase it is the same over η to
  3.5×10⁻¹⁴ in log₁₀, and it falls with \|Q\| (Spearman −0.96 on 3401 plants, −0.96 among those with 0.5 ≤ ρ₂₂ ≤ 2). But it
  stays 12.5–46 times the real series' at every position, so the real shape is outside what the lattice reaches.
- Relocated, the shape is 0.67–0.91 times the real series' at every plant, a spread of 1.4, with a weak fall in \|Q\|
  (Spearman −0.83). That spread is smaller than the real series' own χ₂₂ spread over its far-end bases (2.1, §15.3).
- Held χ₂₀ is large because the zero is held: the real zero was located on l2 at 20 terms (§14), so the held profile
  carries an offset the real one does not (§13.5), which is why the held variant fails where the relocated one passes.
  The 12 positions P′ fails all pass P″ or are unknown under it, (+2,−1) being the only unknown.

## Post-freeze (after the verdict was read; labeled so)

| | held | relocated |
|---|---|---|
| closest approach to the real profile, max over M of \|log₁₀ ρ_M\|, over the plants that pass (a) and (c) at ω∞ | 0.67 at every outer position, window edge 0.699 | 0.05–0.32, except 0.51, 0.71 and 0.49 at (0,0), (0,−1) and (0,−2) |
| drift of ρ_M between ω∞ and another node, 575 and 486 plants run at both | median 0.124, 90th percentile 0.187, max 0.206 decades | median 0.095, 0.116, 0.130 decades |
| unknown plants, and plant-node runs to decide them at most | 678 at 22 positions, 1356 | 2240 at 12 positions, 4475 |
| margin of each unknown position's best candidate at ω∞ | 0.007–0.032 decades | 0.18–0.63 decades |

So the held unknowns pass at ω∞ by at most 0.03 decades, less than a typical node drift, while every relocated unknown
passes by more than the largest drift seen (0.13). This is a heuristic on the plants that were run at several nodes (they
passed (a) and (c) at ω∞), not a verdict: only a run of the other nodes decides them.

## Recommended tasks (full text; the coordinator files them)

1. **Decide P″'s 12 unknown positions.** What: for each of the 12 positions and each group with unknown plants, run the
   plants that pass (a), (c″) and (d″) at ω∞ at 0.99 and then 1.01 in smallest-D″ order until one passes at both
   (`pade_second_ring.py`'s node rule with (d″) added). At most 4475 plant-node runs, about 3 s each on the Mac, usually
   far fewer. Why: it turns the bracket 24–36 of 37 into a number and says whether the relocated profile narrows at
   \|Q\| ≥ 2.48 at all. Accept: every unknown position gets pass or fail; the unmodified rule reproduces #718's
   hits; `--mutate=scale_chi` still fires. Depends on #746. Expected from the margins: none fails.
2. **The profile at fewer terms.** What: χ_M of the ring plants at M = 12–19 against the real series', in zk/chord, at
   one plant per position and group at ω∞ (`Proj.rows(sig, Ms=...)`), held and relocated. Why: at 20–22 terms the located
   zero fits both sets alike (relocated σ within 1.4), so a lower M may be where the second set's position shows, if
   anywhere. Accept: planted truth first (§17.2's edge and J+ pattern at those M), then the verdict by a window frozen
   in the notes before any profile is read. Depends on #746; speculative.
