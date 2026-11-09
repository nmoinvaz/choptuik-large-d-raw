# I257-mac: the alias rule of #242 on hp/modecount_circle.py's arcs, its planted test, and the existing circles re-checked

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27), shared with other sessions.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/257
Code: branch wip/i254 of the code repository, commit b40fa99 (`hp/modecount_circle.py`,
`hp/modecount_circle_planted.py`). Python 3.14.7 (venv-314), hpkernel of 2026-11-08 16:24 PST, modecount_cx from the
main checkout's build of 2026-11-08 16:26 PST (PYTHONPATH). nice 10, caffeinate -i, one process.

## Files

- `logs/planted.log` (exit 0) and `logs/planted_controls.log` (exit 0: the test passes, and the mutations nodiv,
  offset and flat each fail it; flat counts the inside pairs +1 instead of +2).
- `scripts/recheck_circles.py`, `scripts/run_recheck.sh`: every committed circle record replayed from its cache with
  the old rule (must reproduce the record) and then with the alias rule; `recheck.jsonl`, `logs/recheck.log`.
- `scripts/live_circles.py`, `scripts/run_live.sh`: the circles that need new determinants, evaluated on their stored
  backgrounds; `live/<name>/` holds each extended cache and `live_circles.jsonl`; `logs/live_*.log`.
- `first_try/`: the first replay script, which gave a missing point its nearest cached value; its counts of missing
  points cascade from those stand-ins and are not used. Superseded by the version that stops at the first missing point.

## Results (closing summary on the issue)

- Planted: `logs/planted.log` exit 0; `logs/planted_controls.log` exit 0 (flat counts the inside pairs +1, not +2).
- 68 circle records (55 distinct circles) replayed exactly under the old rule. Under the new rule 49 are unchanged from
  their caches alone, and 4 more (#178's R 0.03 at 1.14 and 1.20, #230 kf 23 B at 3.019, #238 D 55 at 0.073+3.839i)
  are unchanged with 1-2 new determinants each (`live/`). Two M 40 circles of #231 need determinants this Mac's
  hpkernel cannot compute (no M 40); `logs/which_part.log` shows which part of the rule asks for them.
