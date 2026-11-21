# I1021-mac/rpi5_loc018: the 2 lower cells of #1013's recount3 (w/w_inf 0.5065-0.6065), windings and the locate

Machine: the Mac, helper session xfchecks, nice 19. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013,
21 Nov 2026. Inputs: `I1013-rpi5-cap/recount3/m3/` at raw 8dafdc05 (points, leaves and count at xi1 0.18; their sheet
check passed, `../sheet_rpi5r3/`, 342b938b). Code: argcount at 6da7da7b (`choptuik-large-d-1021b`).

## Union winding (`union_winding.py`, read-only)

`union_winding.py CODE CACHE LEAVES COUNT` reads the cache with argcount's Multiplier and Counter, and stops if any
point is missing, so it computes nothing. The criteria are in its docstring, written before the run. For each cell of
COUNT with an integer boundary winding and unresolved leaves inside, all of these must hold:

- the cell's winding recomputed from its own boundary equals COUNT's;
- the union U of the unresolved leaves is a rectangle;
- W(U) from U's own boundary is resolved and equals W(cell) minus the sum of the resolved leaves' W.

`--mutate=conj` conjugates every value, so it must fail.

Run 2026-11-21 on a scratch copy of recount3's cache (sha256 a996b964..., unchanged after the run). Log:
`union_winding.log`. Result: PASS, and the control fails (exit 1).

| cell | W (count / own boundary) | resolved leaves, sum | union U of the unresolved leaves | W(U) | min \|R\| on U's boundary |
|---|---|---|---|---|---|
| A 3.8623-4.1123 × w 0.5065-0.6065 | +1 / +1 | 71, 0 | A 4.0498456-4.0810956 × w 0.50654321-0.53154321 (2 leaves) | +1, resolved | 1.42e5 |
| A 4.1123-4.3623 × w 0.5065-0.6065 | −1 / −1 | 66, 0 | A 4.2373456-4.2998456 × w 0.53154321-0.55654321 (4 leaves) | −1, resolved | 5.95e6 |

So at xi1 0.18, U1's boundary winds +1 and U2's winds −1, each from a resolved boundary on one sheet. recount3's
"zeros none" lists zeros of resolved leaves only, and U1 and U2 are not leaves.

What this does not show:

- U1 (0.031 × 0.025) and U2 (0.0625 × 0.025) are larger than argcount's --hzero (0.02), the size below which a leaf
  with W ≠ 0 is taken as one zero. So each union holds net +1 or net −1, not necessarily exactly one zero.
- Splitting them, as argcount does, puts the guard-blocked points (4.063517475, 0.51904321) and
  (4.2685956, 0.54404321) on the children's edges, which is why recount3 left them unresolved.
- The zeros are not located.

## The locate (`run_loc018.sh`, for rpi5; written before the run, on the coordinator's request of 21 Nov)

**When it runs.** On rpi5 after recount4 (`../rpi5_fu018/`), not beside it. recount4 uses all 4 cores: its value
step runs a pool of 4, and its recount runs `--procs=4`. Run it only if recount4 leaves the lower leaves unresolved. If
recount4 lifts a guard-blocked point and resolves those leaves, argcount splits them and locates the zero itself, and
this step is not needed for that cell. Start only on the coordinator's word. The input is recount3's cache, pinned by
sha256. recount4 changes the lower cells only by appending an accepted row for a guard-blocked point, the case above.

**Command**, from rpi5's raw root, with `I1021-mac/rpi5_loc018` present:

    nohup bash I1021-mac/rpi5_loc018/run_loc018.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1013-rpi5-cap/loc018_driver.out 2>&1 &

**Checks before the run.** The driver stops if any of these fails:

- CODE is at 6da7da7b with no changes;
- `I1013-rpi5-cap/loc018` does not exist;
- recount3's points, seed file, leaves and count match `in/SHA256SUMS_recount3`;
- `locate018.py`, `plant_check.py` and `union_winding.py` match `SHA256SUMS`;
- argcount's selftest and its five mutations exit `0 1 1 1 1 1`;
- `locate018.py --selftest` and `plant_check.py --selftest` exit 0. The first runs `check` and `check2` on synthetic
  results, plain and with each mutation, and must give PASS FAIL FAIL twice;
- `union_winding.py` on the cache exits 0, and with `--mutate=conj` it exits 1.

`plant_check.py` is `../final/plant_check.py` at raw cd031fcd, byte for byte.

**Stage 1** (`locate018.py run`, nice 10, 8 h cap, 4 processes):

- argcount's `locate_many` at xi1 0.18, from the centres of U1 (4.0654706, 0.51904321) and U2 (4.2685956, 0.54404321)
  on the plain map. This is Newton on (Re R, Im R) with finite-difference Jacobians, on the unguarded values, at most
  20 steps.
- The control is the same Newton from the centre of C0 = A 3.9560956-3.9717206 × w 0.5565432-0.5690432 on the map
  with a +1 planted at P0 = (3.9623456, 0.5615432), at 0.4 of each of C0's ranges. C0 lies in a resolved W = 0 leaf
  of cell A 3.8623-4.1123, with min |R| 2.19e6 on that leaf's boundary.
- recount3's settings throughout: starts 0.2 then 0.25, bound 1e7, wall 3600 s, noise cap 1e7, seeds from the cache
  and the 0.17 file.

`locate018.py check` must pass, and with `--mutate=shift` and with `--mutate=sign` it must fail, or the run ends.

**Stage 2.** `locate018.py boxes` writes three relocation boxes, each 0.015625 × 0.0125 (both under `--hzero` 0.02):

- B1 and B2, each with stage 1's point at 0.4 of each range;
- C0.

argcount then recounts the three boxes with recount3's arguments, at nice 10, with an 8 h cap per count:

- once plain, tag `M3_loc018_plain_r0.18`;
- once with `--plant=P0`, tag `M3_loc018_plant_r0.18`.

`--r1b=0.17` locates each zero again at 0.17, and that is reported. At the end, `argcount_samebits.py` compares
recount3's cache with loc018's.

**Criteria** (fixed before rpi5's run). The fallback point in 1 and the optional location in 2 were added after the
Mac's dry run, where U1's Newton left the cell's double after 18 steps at its noise floor (below).

1. Stage 1 (`locate018.py check`):
   - for C0 on the planted map, Newton ends within 0.05 of C0's size of P0 in each coordinate, with sign +1;
   - each union U gets a point. It is "located" when Newton ends inside U with Jacobian sign W(U) (U1 +1, U2 −1) and
     |R| at most 10 sigma there. Otherwise it is "nearest": the point of smallest unguarded |R| among the points this
     run computed inside U, if its |R| is at most 10 sigma;
   - exit 0 when C0 passes and both unions have a point, 2 when C0 passes and one has, 1 otherwise. The run goes on
     at 0 or 2, with a box only for a union that has a point;
   - with `--mutate=shift` (P0 moved one box width in A) and with `--mutate=sign`, the check exits 1.
2. Stage 2 (`locate018.py check2` on the plain count):
   - each box B lies inside its union;
   - B winds W(U) (B1 +1, B2 −1), resolved, with no unresolved leaf and exactly one zero, of that sign;
   - if argcount locates that zero, it lies inside B, within 0.1 of B's size of stage 1's point in each coordinate.
     If not, the zero is reported as counted, not located;
   - C0 winds 0, resolved, with no zero;
   - with `--mutate=sign`, the check fails. With `--mutate=shift` it fails when a zero is located, and is vacuous
     otherwise.
3. The plant (`plant_check.py PLANT --record PLAIN --at P0`) passes, and with `--mutate=shift` it fails:
   - one +1 zero whose cell contains P0;
   - C0 winds the plain winding plus 1;
   - B1 and B2 wind as in the plain count;
   - the zeros outside C0 are the plain count's.
4. samebits: every valued record of recount3's cache is unchanged (exit 0).
5. xfchecks' sheet check of loc018's new points (as `../sheet_rpi5r3/`) passes before the result is used.

**What a pass shows.** In each lower cell, a zero of sign W(U), counted in a box under 0.02 that lies inside U. It is
located when argcount's Newton ends there. By additivity, the rest of U (U minus B) then winds 0. It is not checked
for a pair of opposite sign, since argcount's resolution test applies to whole cells only.

**Cost.** Stage 1 needs at most 3 targets × 20 steps × 3 points, and fewer if Newton settles. Stage 2 needs each box's
corners and edge points, plus the locates at 0.17. recount3's points took 132 CPU s on average. That gives a few hours
on 4 processes. The caps bound it at 8 h per step.

**After a zero is located.** Its M = 5 test belongs to #1021's route (z7_m7, xi015d), which waits on the double-double
inner_nb, Nathan's call.

## Dry run (the Mac, 6da7da7b, nice 19, 21 Nov; scratch copies)

- `locate018.py --selftest`, first form: check PASS FAIL FAIL, check2 PASS FAIL FAIL (exit 0). `plant_check.py --selftest`:
  PASS FAIL FAIL FAIL (exit 0).
- The driver refuses, with exit 1, when `loc018/` exists, when an input differs from its sha256 (a line added to
  recount3's count), and when `locate018.py` is changed.
- Stage 1 (`locate018.py run`, 2 processes, 2026-11-21 00:45:10 to 01:37:55 UTC (file times); the first form of the script, which did
  not record the nearest point. It was taken from the run's new cache lines afterwards, as the amended `run` takes it):

  | target | Newton | nearest point of the run inside U | stage 1 |
  |---|---|---|---|
  | U1 | no point: after 18 steps an iterate left the cell's double | (4.0623918, 0.51891094), \|R\| 162, 0.072 sigma, of 53 new points | nearest |
  | U2 | (4.2699839, 0.54447545), sign −1, \|R\| 0.273 sigma | | located |
  | C0, planted | (3.9623456, 0.5615432), P0 to 1e-13, sign +1 | | PASS |

  U1's iterates stay near (4.0624, 0.5189) from the second step on, with |R| down to 162 against sigma about 2.3e3.
  The finite-difference Jacobian at that floor is noisy, so Newton does not settle, and one step jumps out. With the
  amendment, `check` gives exit 0, and `--mutate=shift` and `--mutate=sign` give exit 1. The amended
  `locate018.py --selftest` (check exits for plain, shift, sign, U1 nearest, U1 none: `[0, 1, 1, 0, 2]`; check2 PASS
  FAIL FAIL PASS PASS) exits 0.
- Stage 2 (the driver's two recounts, 2 processes, on the dry run's cache and boxes): running; the result goes here.
