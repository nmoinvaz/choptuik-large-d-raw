# I1005-mac: backup of the choptuik-large-d issues and their comments before they were moved into the GitHub project

Machine: the Apple M5 Mac (`mac`), coordinator session. Task 1005, "Move the repository's issues into the project as
items".

- `issues_with_comments/issue_<n>.json`: each issue that had comments on 2026-11-10 07:45 UTC, as the GitHub REST API
  returned it (`issue`), with its comments in order (`comments`).
- `issues_without_comments/issue_<n>.json`: each issue that had no comment, as the REST API returned it, saved just
  before it was moved.
- `converted.jsonl`, `converted2.jsonl`: one record per issue moved, with the new item's id and its field values.

The items were built from these files' `title`, `body` and comment `body` fields.
