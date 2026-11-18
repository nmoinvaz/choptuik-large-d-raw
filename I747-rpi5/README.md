# I747-rpi5: a pre-registered scan for the far Padé poles alone

Machine: rpi5 (Raspberry Pi 5, 4 cores, 8 GB), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/747

Code: `solver/inner_amp/pade_far_poles.py` of the repository's branch `wip/i747`. Criteria: notes/PADE_FAR_END.md §18, committed
before any plant was judged (fb21b909), with the script after it (10b90d9b).

Files are filled in as the stages run: `control*.log|json` (selftest, J+, J−, the planted poles P, the regression R4, and the
mutations), `plants.jsonl` (every plant record, resumable), `scan.log|json` (stages A to C and the verdict), `report.log`.
