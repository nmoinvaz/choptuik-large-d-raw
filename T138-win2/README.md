# T138-win2: the chain rerun bias-free, harmonics held on the 1/n fit

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main 31da699 (Python
only past 579e403, the T126 octo-double build, no rebuild). venv-t126. 18 threads, below normal. Comms entry:
2026-11-07 01:18 UTC cloud to win2.

T137 showed the chain's large-D gap is the held harmonics' bias (first-step dDelta +5e-8 at D 80 to +3.4e-6 at D 215,
matching the full-system series). T138 reruns the chain with the harmonics held on a 1/n fit of the full-system states
(--held_fit data/held_fit.json, hp/held_fit.py / pinning.HeldFit, notes/HELD_HARMONICS.md) so the bias is removed.

Pilot (3 steps) from D 73, then the full chain if it passes:
  anm_run.py <raw> T138-win2\pilot --state T81/conv_pin5_D73.0000_D73.000000.npz --kfreeze 3
    --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 3 --D_max 1000 --threads 18 --corrector qd
    --tol_qd 1e-28 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
Pilot pass: all 3 steps converge (qd max|F| < 1e-28), and the log prints "held values from the fit data/held_fit.json".
Then the same command into T138-win2\chain with --steps 300, hourly posts. Runner rules: above D 165, when the order-4
series ratio falls below 30, restart with --jet_o 1 (drop --jet_q/--pred_q); when the quad corrector stalls above 1e-28
twice in a row, restart with --corrector od --tol_od 1e-40; hang rule stands; stop after 24 h or three-halvings.

chain/ (quad jet, bias-free) climbed D 73 -> 173.5 cleanly in ~101 full a=1.0 steps (re-seed ~96/5, series far
healthier than the pinned chain: ratios grew to ~210/190 through D 165). Above D 165 the order-4 ratio then fell below
30 (166 at D 165 -> 15.3 at D 170 -> 2.3 at D 173), the escalation trigger. Stopped at 2026-11-07 03:00 UTC.

chain_o/ restarts from chain/anm_pin3_D173.5000.npz with --jet_o 1 (octo jet; drop --jet_q/--pred_q), --corrector qd
unchanged, rest as chain. The octo jet rebuilds the high-order series the quad jet lost. Same stop/escalation rules;
if the qd corrector stalls above 1e-28 twice, next escalate to --corrector od --tol_od 1e-40.
chain_o climbed D 173.5 -> 215.0 cleanly (octo jet + qd corrector, series healthy a_max ~3.4). It was stopped at D 215
for T141, then resumed; at D 215 the resume three-halvings-stopped because the quad corrector stalls above 1e-28
(8.9e-10, 2.4e-17, 3.5e-20 at a=0.5/0.25/0.125), the rule-2 trigger.

chain_od/ restarts from chain_o/anm_pin3_D215.0000.npz with --corrector od --tol_od 1e-40 (the octo-double corrector),
keeping --jet_o 1, rest unchanged. Full octo (octo jet + octo corrector), as T129 chain5. Same stop rules (24 h,
three-halvings, degenerate; hang rule).
