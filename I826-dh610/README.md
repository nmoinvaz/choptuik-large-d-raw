# I826-dh610: Newton from s0_D252's planted truth at the default projection switch (D 252.6135)

Machine dh610, issue https://github.com/nmoinvaz/choptuik-large-d/issues/826. Script (the coordinator): `run826.sh`,
`octo_corrector.py planted` from the truth itself (`--rel 0`), default switch 1e-15, #777's rerun flags otherwise,
`--it_max 12`, 4 threads, in #817's worktree (main 390d1db9) and state copy.

Criteria (#826): pinned max|F| below 1e-40 within 12 steps, with Delta - Delta(truth) in eight parts; otherwise the step
where it stops, with its trials. The first step must reproduce #823's dDelta +3.311085e-8 to 1e-12 relative, else
stop and report.
