# I667-mac: plants with a weak second singular set past S₁'s arc, judged on DA2, the far Padé poles and the twin test

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/667

Code: `solver/inner_amp/pade_second_set.py` on the branch `wip/i667-subagent` of nmoinvaz/choptuik-large-d. Method and
frozen criteria: `notes/PADE_FAR_END.md` section 12.

- `selftest*.log`: the second set's exact moments against `mpmath.quad`, the projected twin residuals against
  `pade_twin_count.lsq`, the agreement count on planted zeros, and the mutations `secmom`, `nest`, `agree` (each must
  fail).
- `control.*`: R1–R4 (the real series' DA2 count, #541's poles, #684's χ at 22 terms by projection, the η = 0 plants
  against FarPlant), J+ (the real series judged as a plant) and J− (the η = 0 plants).
- `control_mutate_col.*`, `control_mutate_judge.*`: the control mutations (each must fail as frozen).
- `grid.*`: the 1584 plants at ω/ω∞ = 1.00, and the other two nodes for the passing and the 20 closest plants.
  `grid.jsonl` holds one full record per plant and node (the DA2 members' zeros, the Padé poles nearest #541's, every
  twin scan), `grid.json` the summary and the verdict.
