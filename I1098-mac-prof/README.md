# I1098-mac-prof: where a release outer step spends its time at D 4000, term by term and with relaxed horizon sums

Machine: this Mac (Apple M5, 10 cores, 32 GB, macOS 27.0.1), shared with other sessions (load 10-17), nice 10.
Issues: https://github.com/nmoinvaz/choptuik-large-d/issues/1098, https://github.com/nmoinvaz/choptuik-large-d/issues/1096

Code: `hp/prof_release.py` on choptuik-large-d branch `wip/large-d-fastmul2` (from `wip/large-d-form-s` b9a2954b),
run on the dev-o1 build of `wip/large-d-fastmul` (0d5c6b99's Rust: the tip's Rust without FS_MAGSTATS and M 48,
which change no cost). Timing ratios only; a dev-o1 build is slower than release.

State (input, read-only): raw `I1088-mac-a/form_s/L4000q/lastnode_D4000.0000.npz`, blob
f06d04d5b98e1df5b8040c263ea50d5e882f60f7 (raw 0c237b561); D 4000, a 9.995, ks 5218, 572 Taylor steps. The formula ks
⌈1.1 (n/2)/(1 − t_l)⌉ + 200 is 2602 here.

- `prof.jsonl`, `prof.log`: one line per measurement (4 threads).

## The Jacobian check (step 3), written 2026-11-26 09:30 UTC before the run

`form_s_relaxed.py jaccheck` (wip/large-d-fastmul2) on the dev-o1 build of that branch, at the D 2000 state of
`I1096-mac/README.md` (ks 2618): the Jacobian's horizon rows in the columns of m_h points 0, 15, 31 and of Delta (4
column tasks, each the horizon series in Du, Qu or Ou lanes), in double-, quad- and octo-double, relaxed against term
by term, relative to max |J| of those columns. Bars: octo-double |J_relaxed − J_naive| <= 1e-110; double- and
quad-double the same 1e-28 and 1e-58, or |J_relaxed − J_od| <= 2 |J_naive − J_od| (amendment 1 of I1096-mac). Control:
relaxed with the first square of c U left out (mutate 56) must miss both. Output `jaccheck.jsonl`, `jaccheck.log`.
