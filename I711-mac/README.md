# I711-mac: the jet estimator on a planted series with #685's three singularity tracks fixed in D

Machine mac (Apple M5), issue https://github.com/nmoinvaz/choptuik-large-d/issues/711. Code: main 78fd43c4, `hp/jet_singularity.py planted --case T3`, whose docstring fixed the criteria before the first run. Python 3.14 (venv-314), mpmath at 80 digits, one process.

The plant holds #685's tracks A (255.71 + 4.99i), B (252.31 + 5.80i) and C (259.20 + 2.88i) as fixed conjugate pole pairs, seen from #685's five bases D0 = 252.2497 to 253.7139. Mix o12 sets the pairs' terms equal at order 12 at the middle base, and mix o24 at order 24.

| run | exit | Padé (judged) | recurrence fit's Im D* over the five bases | verdict |
|---|---|---|---|---|
| `planted_T3.log` | 1 | o12: all three pairs at every base; o24: A missed at the last three bases, B at one | o12 5.36, 4.03, 0.00, 1.80, 2.40 (fall 2.96); o24 3.63, 0.00, 0.00, 0.00, 2.74 (fall 0.88) | DRIFTS |
| `planted_T3_mutate_drop_pole.log` (A left out, the control) | 1 | A not found at every base in o12, where the unmutated run passes | | the control fires |

So three singularities that do not move make the two-term recurrence fit's D* reach the real axis and wander, as it does on #685's real series. By the rule fixed before the run, #685's recurrence reading is dropped. Padé recovers all three pairs when their terms are balanced at order 12 (o12). When C dominates the low orders (o24), it misses the nearest pair A, so the plant fails its own pass criterion.
