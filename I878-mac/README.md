# I878-mac: fixed_point_M_b.py reads --x at the working precision, and the 38 stored runs keep their verdicts

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/878 (finding F2
of the review #867, proof/A_M_b_review.md). Code: branch `wip/sa-878` on main dacbb5d8, the fix and the new harness command
at 01553291, one line of proof/A_lemmas_M.md §2.5 at 9ee9ad0d.

## The change

`fixed_point_M_b.main()` now sets `ctx.prec` right after it reads `--prec`, before `--x`, `--box` or `--cbox`
becomes a ball. That is one added line; no bound and no other function changes. The harness gains
`fixed_point_M_b_check.py cli`.

## Results

`exits.txt` lists the five checks; each log is `<name>.log`, and `rerun/` holds the 38 logs and their own
`exits.txt`.

| check | what must hold | result |
|---|---|---|
| plain_M5: `python3 fixed_point_M_b.py --M=5 --x=<p̂ of data/A_M2_box_M5_1e-10.json>` | N = 105, k = 103, constant 0.1000 | N = 105, k = 103, 0.1000; sup\|η\| at \|z\| = R: p 4.34×10⁻⁸⁷, v 8.49×10⁻⁸⁵, c 8.42×10⁻⁹¹ |
| cli: the command line as a subprocess against `Setup` and `prove` on the point read at 512 bits | equal N, k and constant | equal: 105, 103, 0.1000 |
| cli_mut_read53 (control): the comparison made with the point read at 53 bits | must differ, exit 3 | differs: 78, 76, 0.1250 for the ball of radius 6.0×10⁻¹⁷; exit 3 |
| rv_cli_precision: the reviewer's check, unchanged | exit 0 | exit 0: both readings prove the contraction, N = 78 against 105, the guard on k refuses k = N − 1 |
| rerun: `review_867/rerun_runs.sh`, the 32 runs of `I427-mac` and the 6 of `I866-mac` | every exit status as required | 38 runs, 0 with another status: 20 exit 0 and 18 exit 3 |

Every one of the 38 rerun logs equals the stored log of the same run (`I427-mac/`, `I866-mac/`) once wall times and
absolute paths are removed. So the fix changes no stored verdict and no stored number, as expected: none of those runs
goes through the plain path.

Before the fix the plain command printed N = 78, k = 76 and 0.1250 (the review's table). The reviewer's script still
shows that pair of readings, because it builds the 53-bit point itself.

## Recommended tasks

None.
