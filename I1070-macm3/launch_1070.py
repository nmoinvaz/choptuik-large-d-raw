#!/usr/bin/env python3
"""#1070 macm3b: start a command in its own session, so that ending the terminal (or the claude session) cannot end it.
Double fork with setsid: the command's parent is launchd (pid 1), it has no controlling terminal, stdin is /dev/null, stdout and stderr go to OUTFILE.
Usage: launch_1070.py OUTFILE [NAME=VALUE ...] -- CMD ARGS...     Prints the command's pid."""
import os, sys
i = sys.argv.index("--"); out = sys.argv[1]; env = dict(os.environ); env.update(a.split("=", 1) for a in sys.argv[2:i]); cmd = sys.argv[i + 1:]
r, w = os.pipe()
if os.fork() == 0:
    os.setsid()
    if os.fork() == 0:
        os.close(r)
        os.write(w, f"{os.getpid()}\n".encode()); os.close(w)
        fd = os.open("/dev/null", os.O_RDONLY); os.dup2(fd, 0)
        fo = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644); os.dup2(fo, 1); os.dup2(fo, 2)
        os.chdir("/")
        os.execvpe(cmd[0], cmd, env)
    os._exit(0)
os.close(w); pid = os.read(r, 32).decode().strip(); os.wait()
print(pid)
