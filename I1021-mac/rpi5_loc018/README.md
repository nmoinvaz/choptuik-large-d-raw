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

## Next: the locate (not yet written)

Newton on (Re R, Im R) from each union's centre, with argcount's `locate_many` on the unguarded values, at xi1 0.18.
This is argcount's own step 4, applied to U1 and U2. To be written with its criteria fixed first, and run only on the
coordinator's word.
