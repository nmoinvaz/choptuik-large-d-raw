p = "README.md"
t = open(p, encoding="utf-8", newline="").read()
reps = [
("(CRLF line endings from Windows Python, the last line `exit N` has LF)",
 "(Windows Python wrote CRLF line endings in the runner's folder; git stores them with LF, see Observations)"),
("- The Windows logs have CRLF line endings (Python text mode on Windows) and a final `exit N` line with LF; the comparison strips `\r`. The logs are therefore not byte-identical to rpi5's, they are identical line by line after removing `\r` and masking the tuned timings. The tuned tables print the Greek letter nu as UTF-8 on both machines.",
 "- Line endings: the runner's folder holds the logs with CRLF (Python text mode on Windows; the final `exit N` line has LF), so `compare1039.py` strips `\r` and the comparison above is line by line. The push worktree has `core.autocrlf=true`, so git stores the logs with LF. As stored in git (this commit), the six logs of `route3_bound_*` are byte-identical to I1030-rpi5's (checked with `cmp` on the two blobs of each), and the two tuned logs differ from rpi5's only in the timing numbers. The tuned tables print the Greek letter nu as UTF-8 on both machines."),
]
for a, b in reps:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok")
