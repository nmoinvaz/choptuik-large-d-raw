# I1086-mac: logs of the large-D basics review (exponents, slow manifold, free-field selection, ks and plan checks)

Machine: the Mac (coordinator's machine), one process at nice 10. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1086.
The note is `notes/LARGE_D_BASICS.md` on branch `wip/large-d-basics` of the main repository; the scripts are in its
`solver/basics/`.

Made by `bash solver/basics/run_all.sh OUT STATES PYTHON` (Python 3.14, the Mac's venv-314) from the main repository's root
(commit b716b2fe), with STATES a `git archive` of these raw folders at 0945bf329: I603-win2/chain, I603-win2/chain_nsr,
I841-dh370/chain, I903-macm3/chain_k135, I903-mac/chain_fixed, I966-dh370/ks_chain3b, I461-win2/crawlB5,
I461-win2/crawlC. The scratch prefix of the state paths is removed from the logs. No state was changed and no solve
was run; every number is read from stored states, `hp/data/delta_all.csv` or closed forms.

| log | what | control |
|---|---|---|
| derive.txt | sympy checks 1–5 (exponents, slow solution, eikonal, free field) | `--mutate=1..5`, each fails |
| free_field.txt | F's weight at x* = 1/√2 against j and n | free_field_mutate_A.txt |
| order_laws.txt, order_laws_tails*.txt | ks for the mass-mode tail, gains in digits, Taylor steps | *_mutate_binom.txt |
| sigma_vs_ks_ref_*.txt | σ_R per state, Δ against a reference chain's spline | ..._mutate_g.txt |
| slow_check.txt | states against the leading-order slow solution, harmonics | slow_check_mutate_K2.txt |
| plan_stability.txt | stored Taylor plans against the fast modes | plan_stability_mutate_h2.txt |
| eeg_gap.txt | chain and EEG26b against the D ≤ 61 1/D fits | eeg_gap_mutate_shift.txt |
| chain_vs_dd_fit.txt | every stored chain state against the D ≤ 61 1/D fits | (eeg_gap's) |
| oscillation_fit*.txt | the order-293 chain's growing oscillation | oscillation_fit_mutate_shuffle.txt |
