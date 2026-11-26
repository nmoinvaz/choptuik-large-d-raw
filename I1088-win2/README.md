# I1088-win2: form-S direct solves at large D (#1088)

Machine win2 (Windows 11, Core Ultra 7 265K, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1088.

Build for these runs: hp from origin/wip/large-d-form-s, built on win2 in `D:\choptuik-formsq` (venv-formsq); its build log, memory samples and selftests are in `I1025-win2/hp_form_s_build/`.

| folder | holds |
|---|---|
| `L8000/` | D 8000 held at L = 20, direct solve (the coordinator's order of 26 Nov): prepared and queued on win2, **cancelled 02:52 UTC, the solve moved to the Mac mini**; holds the README, the pinned guess, the driver and the gate script, no run |
