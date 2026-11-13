# I548-mac: chord against arc from σ₀–σ₂₂, three discriminators judged on plants, and the noise-scale bound

Machine: mac (the coordinator's Apple M5), one core under `nice -n 10`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/548

Made by `solver/inner_amp/pade_chord_arc.py` of the code repository (branch `wip/i547-subagent`). Method and frozen
criteria: `notes/PADE_FAR_END.md` §5 there.

| file | what |
|---|---|
| `selftest.log` | the selftest and its two mutations |
| `plants.json`, `plants.log` | H_DA, H_HP and R_w on chord2 and arcjump at three nodes, and arcmid, arcsteps and arc, with noise spreads |
| `plants_mutate_mirror.*` | the mirror mutation (arc profile reflected across the chord) |
| `plants_mutate_sigma7.*` | σ₇ × 1.01, reported |
| `bound.json`, `bound.log`, `plants_noise*.json` | the noise-scale study, measured errors × 1 … 10⁻⁴, and its per-scale records |
| `twin.json`, `twin.log` | chord twins (two branch points, M-term density on the chord) fitted to arcjump's σ₀–σ₂₂, χ against the measured errors |
| `twin_mutate_twin_noshift.*` | the twin's control: fitted to chord2 itself, reproduced at M = 6 |
