# choptuik-large-d-raw

Raw run output of [choptuik-large-d](https://github.com/nmoinvaz/choptuik-large-d): solver states (npz), per-point
records (jsonl), attempts files, checkpoints and logs, one folder per task. The code repository keeps only what is
derived from them (CSVs, graphs, notes), naming the folder and commit where it uses them. [INDEX.md](INDEX.md) lists
every folder and what it holds. [MOVED_FROM_MAIN.md](MOVED_FROM_MAIN.md) lists the files removed from the code
repository's main because this repository holds the same content.

## Layout

- One folder per task and machine: `<task>-<machine>/`, for example `T82-win/` or `T83-mac/`. A task run on two
  machines has two folders.
- Every folder starts with a `README.md` whose first line is `# <folder>: <what it holds>`, followed by the machine,
  the source directory or worktree, and the comms.txt entry or commands that produced it.
- The folders imported from the code repository's `raw/<name>` branches on 2026-10-27 keep the branch's name (`T75/`
  from `raw/T75`) and its commits: a citation such as "raw/T76 7ca90fe" resolves here as commit `7ca90fe` (with the
  files at that commit's root). Each branch came in by a merge commit, "Import raw/<name> (<last commit>)", whose
  second parent is the branch: `git log <merge>^2` shows the branch's history. `git log -- T75` starts at that merge,
  since the branch's own commits hold the files at the root, not under `T75/`.

## Adding output

Clone this repository next to the code checkout, once:

    git clone https://github.com/nmoinvaz/choptuik-large-d-raw ../choptuik-large-d-raw

Point the run's output paths into its folder (the code's writers refuse a path outside a folder of this repository;
`hp/raw_out.py`). Write the folder's `README.md` before the run. At each post, from this repository's root:

    python3 make_index.py
    git add <folder> INDEX.md && git commit -m "<folder>: ..."
    git pull --no-rebase && git push

If the pull reports a conflict in `INDEX.md`, run `python3 make_index.py`, `git add INDEX.md` and commit; the index is
generated, so that resolves it.

## Rules

- Only the output of this project's tasks. Nothing from another project's directories, no credentials, keys, tokens,
  browser or shell data, and no personal files.
- No file over 90 MB (GitHub refuses 100 MB).
- Add to your own folder only. Never delete or rewrite another folder, never force-push, never rebase.
- `python3 make_index.py --check` exits 1 when `INDEX.md` is stale or a folder's README lacks its title line.
